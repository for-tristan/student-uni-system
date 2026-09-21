from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.main import app, load_data
from src.data.preprocessing import (
    build_student_profile,
    get_completed_course_ids,
    load_courses,
    load_enrollments,
    load_students,
)
from src.evaluation.metrics import run_evaluation
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


@pytest.fixture(scope="module")
def client() -> TestClient:
    load_data()
    with TestClient(app) as c:
        yield c


def test_full_pipeline_data_loading(students, courses, enrollments) -> None:
    assert len(students) > 0
    assert len(courses) > 0
    assert len(enrollments) > 0
    assert "student_id" in students.columns
    assert "course_id" in courses.columns
    assert "status" in enrollments.columns


def test_full_pipeline_profile_building(students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    assert profile["student_id"] == 1
    assert isinstance(profile["interests"], list)
    assert isinstance(profile["skills"], list)
    assert isinstance(profile["completed_course_ids"], list)


def test_full_pipeline_baseline_recommender(students, courses, enrollments) -> None:
    recs = baseline_recommend(1, students, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    completed = set(get_completed_course_ids(enrollments, 1))
    for r in recs:
        assert r.course_id not in completed
        assert 0.0 <= r.score <= 1.0
        assert len(r.reasons) > 0


def test_full_pipeline_ml_recommender(students, courses, enrollments) -> None:
    recs = ml_recommend(1, students, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    completed = set(get_completed_course_ids(enrollments, 1))
    for r in recs:
        assert r.course_id not in completed
        assert 0.0 <= r.score <= 1.0
        assert len(r.reasons) > 0


def test_full_pipeline_prerequisite_filtering(students, courses, enrollments) -> None:
    from src.data.preprocessing import parse_prerequisites
    completed = set(get_completed_course_ids(enrollments, 1))
    recs = baseline_recommend(1, students, courses, enrollments, top_n=20)
    for r in recs:
        row = courses.loc[courses["course_id"] == r.course_id].iloc[0]
        prereqs = parse_prerequisites(row["prerequisites"])
        for p in prereqs:
            assert p in completed


def test_full_pipeline_explanations_are_data_driven(students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    recs = baseline_recommend(1, students, courses, enrollments, top_n=5)
    profile_skills = {s.lower() for s in profile["skills_with_history"]}
    profile_interests = {i.lower() for i in profile["interests"]}
    for r in recs:
        for reason in r.reasons:
            if "interest" in reason.lower():
                assert any(i in reason.lower() for i in profile_interests)
            elif "skill" in reason.lower():
                assert any(s in reason.lower() for s in profile_skills)


def test_full_pipeline_evaluation_runs(students, courses, enrollments) -> None:
    results = run_evaluation(k_values=[5], hide_ratio=0.3, seed=42)
    assert "baseline" in results
    assert "ml" in results
    assert results["baseline"]["metrics"]["n_students_evaluated"] > 0


def test_full_pipeline_api_endpoints(client: TestClient) -> None:
    root = client.get("/")
    assert root.status_code == 200
    health = client.get("/health")
    assert health.status_code == 200
    recs = client.get("/recommendations/1?top_n=3")
    assert recs.status_code == 200
    data = recs.json()
    assert data["student_id"] == 1
    assert len(data["recommendations"]) <= 3


def test_full_pipeline_api_error_handling(client: TestClient) -> None:
    invalid = client.get("/recommendations/99999")
    assert invalid.status_code == 404


def test_full_pipeline_all_students_recommendable(students, courses, enrollments) -> None:
    for sid in students["student_id"].tolist():
        recs = ml_recommend(sid, students, courses, enrollments, top_n=1)
        assert isinstance(recs, list)


def test_full_pipeline_deterministic(students, courses, enrollments) -> None:
    a = baseline_recommend(1, students, courses, enrollments, top_n=5)
    b = baseline_recommend(1, students, courses, enrollments, top_n=5)
    assert [r.course_id for r in a] == [r.course_id for r in b]
    c = ml_recommend(1, students, courses, enrollments, top_n=5)
    d = ml_recommend(1, students, courses, enrollments, top_n=5)
    assert [r.course_id for r in c] == [r.course_id for r in d]
