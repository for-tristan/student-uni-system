from __future__ import annotations

from typing import Dict, List, Sequence, Set

import numpy as np
import pandas as pd

from src.data.preprocessing import (
    build_student_profile,
    get_completed_course_ids,
    load_courses,
    load_enrollments,
    load_students,
)
from src.models.baseline import recommend_courses as baseline_recommend
from src.models.recommender import recommend_courses as ml_recommend


def precision_at_k(recommended: Sequence[int], relevant: Set[int], k: int = 5) -> float:
    if k <= 0:
        return 0.0
    top_k = list(recommended)[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for r in top_k if r in relevant)
    return hits / k


def recall_at_k(recommended: Sequence[int], relevant: Set[int], k: int = 5) -> float:
    if not relevant:
        return 0.0
    if k <= 0:
        return 0.0
    top_k = list(recommended)[:k]
    hits = sum(1 for r in top_k if r in relevant)
    return hits / len(relevant)


def average_precision(recommended: Sequence[int], relevant: Set[int]) -> float:
    if not relevant:
        return 0.0
    score = 0.0
    hits = 0
    for i, item in enumerate(recommended, start=1):
        if item in relevant:
            hits += 1
            score += hits / i
    return score / len(relevant)


def mean_average_precision(
    recommendations: List[Sequence[int]], relevants: List[Set[int]]
) -> float:
    if not recommendations:
        return 0.0
    aps = [average_precision(rec, rel) for rec, rel in zip(recommendations, relevants)]
    return float(np.mean(aps))


def evaluate_recommender(
    recommend_fn,
    students: pd.DataFrame,
    courses: pd.DataFrame,
    enrollments: pd.DataFrame,
    k_values: List[int] | None = None,
    hide_ratio: float = 0.3,
    seed: int = 42,
) -> Dict:
    if k_values is None:
        k_values = [5, 10]

    rng = np.random.default_rng(seed)
    metrics: Dict[str, float] = {}
    per_student: List[Dict] = []

    all_precisions: Dict[int, List[float]] = {k: [] for k in k_values}
    all_recalls: Dict[int, List[float]] = {k: [] for k in k_values}
    all_aps: List[float] = []

    for _, student in students.iterrows():
        sid = int(student["student_id"])
        completed = get_completed_course_ids(enrollments, sid)
        if len(completed) < 3:
            continue

        n_hide = max(1, int(len(completed) * hide_ratio))
        hidden = set(rng.choice(completed, size=n_hide, replace=False).tolist())
        remaining = set(completed) - hidden

        masked_enrollments = enrollments.copy()
        mask = (
            (masked_enrollments["student_id"] == sid)
            & (masked_enrollments["course_id"].isin(hidden))
        )
        masked_enrollments = masked_enrollments.loc[~mask].copy()

        try:
            recs = recommend_fn(sid, students, courses, masked_enrollments, top_n=max(k_values))
        except KeyError:
            continue
        except Exception:
            continue

        recommended_ids = [r.course_id for r in recs]
        relevant = hidden

        for k in k_values:
            all_precisions[k].append(precision_at_k(recommended_ids, relevant, k))
            all_recalls[k].append(recall_at_k(recommended_ids, relevant, k))

        all_aps.append(average_precision(recommended_ids, relevant))

        per_student.append({
            "student_id": sid,
            "hidden_count": len(hidden),
            "recommended": recommended_ids,
            "relevant": sorted(relevant),
            "precision@5": precision_at_k(recommended_ids, relevant, 5),
            "recall@5": recall_at_k(recommended_ids, relevant, 5),
            "precision@10": precision_at_k(recommended_ids, relevant, 10),
            "recall@10": recall_at_k(recommended_ids, relevant, 10),
            "ap": average_precision(recommended_ids, relevant),
        })

    for k in k_values:
        metrics[f"precision@{k}"] = float(np.mean(all_precisions[k])) if all_precisions[k] else 0.0
        metrics[f"recall@{k}"] = float(np.mean(all_recalls[k])) if all_recalls[k] else 0.0
    metrics["map"] = float(np.mean(all_aps)) if all_aps else 0.0
    metrics["n_students_evaluated"] = len(per_student)

    return {
        "metrics": metrics,
        "per_student": per_student,
    }


def run_evaluation(
    k_values: List[int] | None = None,
    hide_ratio: float = 0.3,
    seed: int = 42,
) -> Dict:
    if k_values is None:
        k_values = [5, 10]

    students = load_students()
    courses = load_courses()
    enrollments = load_enrollments()

    baseline_result = evaluate_recommender(
        baseline_recommend, students, courses, enrollments,
        k_values=k_values, hide_ratio=hide_ratio, seed=seed,
    )
    ml_result = evaluate_recommender(
        ml_recommend, students, courses, enrollments,
        k_values=k_values, hide_ratio=hide_ratio, seed=seed,
    )

    return {
        "baseline": baseline_result,
        "ml": ml_result,
        "config": {
            "k_values": k_values,
            "hide_ratio": hide_ratio,
            "seed": seed,
            "n_students": len(students),
            "n_courses": len(courses),
            "n_enrollments": len(enrollments),
        },
    }


def format_report(results: Dict) -> str:
    lines: List[str] = []
    config = results["config"]
    lines.append("=" * 60)
    lines.append("Recommendation System Evaluation Report")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Dataset:")
    lines.append(f"  Students:     {config['n_students']}")
    lines.append(f"  Courses:      {config['n_courses']}")
    lines.append(f"  Enrollments:  {config['n_enrollments']}")
    lines.append("")
    lines.append("Methodology:")
    lines.append(f"  Hide ratio:        {config['hide_ratio']:.0%} of completed courses hidden")
    lines.append(f"  Seed:              {config['seed']}")
    lines.append(f"  K values:          {config['k_values']}")
    lines.append(f"  Evaluated students: {results['baseline']['metrics']['n_students_evaluated']}")
    lines.append("")
    lines.append("-" * 60)
    lines.append(f"{'Metric':<20} {'Baseline':>15} {'TF-IDF ML':>15}")
    lines.append("-" * 60)

    bm = results["baseline"]["metrics"]
    mm = results["ml"]["metrics"]
    metric_keys = [k for k in bm if k != "n_students_evaluated"]
    for key in metric_keys:
        lines.append(f"{key:<20} {bm[key]:>15.4f} {mm[key]:>15.4f}")
    lines.append("-" * 60)
    lines.append("")
    lines.append("Limitations:")
    lines.append("  - Synthetic dataset with 25 students may produce noisy metrics.")
    lines.append("  - Hide-ratio methodology biases toward courses the student already")
    lines.append("    completed, which may not represent true future interests.")
    lines.append("  - Recall is bounded by the number of hidden courses per student.")
    lines.append("  - Precision@K can be 0 for students whose hidden courses are not")
    lines.append("    recommendable due to prerequisite chains.")
    lines.append("=" * 60)
    return "\n".join(lines)


def save_report(report_text: str, path: str = "evaluation_report.txt") -> None:
    from pathlib import Path
    out = Path(path)
    out.write_text(report_text, encoding="utf-8")
