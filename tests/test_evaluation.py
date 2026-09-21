from __future__ import annotations

import pandas as pd
import pytest

from src.data.preprocessing import load_courses, load_enrollments, load_students
from src.evaluation.metrics import (
    average_precision,
    evaluate_recommender,
    format_report,
    mean_average_precision,
    precision_at_k,
    recall_at_k,
    run_evaluation,
    save_report,
)
from src.models.baseline import recommend_courses as baseline_recommend
from src.models.recommender import recommend_courses as ml_recommend


@pytest.fixture(scope="module")
def students() -> pd.DataFrame:
    return load_students()


@pytest.fixture(scope="module")
def courses() -> pd.DataFrame:
    return load_courses()


@pytest.fixture(scope="module")
def enrollments() -> pd.DataFrame:
    return load_enrollments()


def test_precision_at_k_perfect() -> None:
    recommended = [1, 2, 3, 4, 5]
    relevant = {1, 2, 3, 4, 5}
    assert precision_at_k(recommended, relevant, k=5) == 1.0


def test_precision_at_k_partial() -> None:
    recommended = [1, 2, 3, 4, 5]
    relevant = {1, 3}
    assert precision_at_k(recommended, relevant, k=5) == pytest.approx(0.4)


def test_precision_at_k_no_hits() -> None:
    recommended = [1, 2, 3, 4, 5]
    relevant = {99, 100}
    assert precision_at_k(recommended, relevant, k=5) == 0.0


def test_precision_at_k_empty_recommended() -> None:
    assert precision_at_k([], {1, 2}, k=5) == 0.0


def test_precision_at_k_empty_relevant() -> None:
    assert precision_at_k([1, 2, 3], set(), k=5) == 0.0


def test_precision_at_k_truncates_to_k() -> None:
    recommended = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    relevant = {1, 2, 3, 4, 5}
    assert precision_at_k(recommended, relevant, k=5) == 1.0
    assert precision_at_k(recommended, relevant, k=10) == 0.5


def test_precision_at_k_zero_k() -> None:
    assert precision_at_k([1, 2, 3], {1}, k=0) == 0.0


def test_recall_at_k_perfect() -> None:
    recommended = [1, 2, 3, 4, 5]
    relevant = {1, 2}
    assert recall_at_k(recommended, relevant, k=5) == 1.0


def test_recall_at_k_partial() -> None:
    recommended = [1, 2, 3]
    relevant = {1, 2, 3, 4, 5}
    assert recall_at_k(recommended, relevant, k=5) == pytest.approx(0.6)


def test_recall_at_k_no_hits() -> None:
    recommended = [1, 2, 3, 4, 5]
    relevant = {99, 100}
    assert recall_at_k(recommended, relevant, k=5) == 0.0


def test_recall_at_k_empty_relevant() -> None:
    assert recall_at_k([1, 2, 3], set(), k=5) == 0.0


def test_recall_at_k_empty_recommended() -> None:
    assert recall_at_k([], {1, 2}, k=5) == 0.0


def test_average_precision_perfect() -> None:
    recommended = [1, 2, 3]
    relevant = {1, 2, 3}
    assert average_precision(recommended, relevant) == 1.0


def test_average_precision_partial() -> None:
    recommended = [1, 4, 2, 5, 3]
    relevant = {1, 2, 3}
    ap = average_precision(recommended, relevant)
    assert 0.0 < ap < 1.0


def test_average_precision_empty_relevant() -> None:
    assert average_precision([1, 2, 3], set()) == 0.0


def test_mean_average_precision() -> None:
    recs = [[1, 2, 3], [4, 5, 6]]
    rels = [{1, 2, 3}, {4, 5, 6}]
    assert mean_average_precision(recs, rels) == 1.0


def test_mean_average_precision_empty() -> None:
    assert mean_average_precision([], []) == 0.0


def test_evaluate_recommender_baseline(students, courses, enrollments) -> None:
    result = evaluate_recommender(
        baseline_recommend, students, courses, enrollments,
        k_values=[5, 10], hide_ratio=0.3, seed=42,
    )
    assert "metrics" in result
    assert "per_student" in result
    metrics = result["metrics"]
    for key in ("precision@5", "recall@5", "precision@10", "recall@10", "map"):
        assert key in metrics
        assert 0.0 <= metrics[key] <= 1.0
    assert metrics["n_students_evaluated"] > 0


def test_evaluate_recommender_ml(students, courses, enrollments) -> None:
    result = evaluate_recommender(
        ml_recommend, students, courses, enrollments,
        k_values=[5, 10], hide_ratio=0.3, seed=42,
    )
    metrics = result["metrics"]
    for key in ("precision@5", "recall@5", "precision@10", "recall@10", "map"):
        assert 0.0 <= metrics[key] <= 1.0


def test_evaluate_recommender_deterministic(students, courses, enrollments) -> None:
    r1 = evaluate_recommender(baseline_recommend, students, courses, enrollments, seed=42)
    r2 = evaluate_recommender(baseline_recommend, students, courses, enrollments, seed=42)
    assert r1["metrics"]["precision@5"] == r2["metrics"]["precision@5"]
    assert r1["metrics"]["recall@5"] == r2["metrics"]["recall@5"]


def test_evaluate_recommender_handles_small_student(students, courses, enrollments) -> None:
    small_students = students.head(3)
    result = evaluate_recommender(
        baseline_recommend, small_students, courses, enrollments, seed=42
    )
    assert "metrics" in result


def test_run_evaluation_returns_both(students, courses, enrollments) -> None:
    results = run_evaluation(k_values=[5], hide_ratio=0.3, seed=42)
    assert "baseline" in results
    assert "ml" in results
    assert "config" in results
    assert results["config"]["k_values"] == [5]
    assert results["config"]["hide_ratio"] == 0.3


def test_format_report_contains_metrics() -> None:
    results = {
        "baseline": {"metrics": {"precision@5": 0.3, "recall@5": 0.2, "precision@10": 0.25, "recall@10": 0.3, "map": 0.15, "n_students_evaluated": 10}},
        "ml": {"metrics": {"precision@5": 0.4, "recall@5": 0.25, "precision@10": 0.3, "recall@10": 0.35, "map": 0.2, "n_students_evaluated": 10}},
        "config": {"k_values": [5, 10], "hide_ratio": 0.3, "seed": 42, "n_students": 25, "n_courses": 40, "n_enrollments": 149},
    }
    report = format_report(results)
    assert "precision@5" in report
    assert "recall@5" in report
    assert "Baseline" in report
    assert "TF-IDF ML" in report
    assert "Limitations" in report


def test_save_report(tmp_path) -> None:
    report_text = "test report"
    path = str(tmp_path / "report.txt")
    save_report(report_text, path)
    with open(path) as f:
        assert f.read() == "test report"


def test_per_student_records_structure(students, courses, enrollments) -> None:
    result = evaluate_recommender(
        baseline_recommend, students, courses, enrollments, seed=42
    )
    for record in result["per_student"]:
        assert "student_id" in record
        assert "hidden_count" in record
        assert "recommended" in record
        assert "relevant" in record
        assert "precision@5" in record
        assert "recall@5" in record
