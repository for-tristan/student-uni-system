from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.preprocessing import (
    build_student_profile,
    get_completed_course_ids,
    load_courses,
    load_enrollments,
    load_students,
)
from src.models.baseline import recommend_courses as baseline_recommend
from src.models.recommender import recommend_courses as ml_recommend
from src.evaluation.metrics import format_report, run_evaluation


def section(title: str) -> None:
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def show_student(student_id: int, students, courses, enrollments) -> None:
    student = students.loc[students["student_id"] == student_id].iloc[0]
    print(f"\nStudent {student_id}: {student['name']}")
    print(f"  Year:   {student['year']}")
    print(f"  Major:  {student['major']}")
    print(f"  Interests: {student['interests']}")
    print(f"  Skills:    {student['skills']}")
    completed = get_completed_course_ids(enrollments, student_id)
    print(f"  Completed courses: {completed}")


def show_recommendations(label: str, recs) -> None:
    print(f"\n--- {label} ---")
    if not recs:
        print("  (no recommendations)")
        return
    for i, r in enumerate(recs, start=1):
        print(f"  {i}. [{r.score:.3f}] {r.course_name} (course_id={r.course_id})")
        for reason in r.reasons:
            print(f"       - {reason}")


def run_demo() -> None:
    section("University Course Recommendation System - Demo")

    students = load_students()
    courses = load_courses()
    enrollments = load_enrollments()

    section("1. Dataset Overview")
    print(f"  Students:     {len(students)}")
    print(f"  Courses:      {len(courses)}")
    print(f"  Enrollments:  {len(enrollments)}")
    print(f"  Categories:   {sorted(courses['category'].unique().tolist())}")

    section("2. Pipeline Verification: Student 1 (Aisha, AI focus)")
    show_student(1, students, courses, enrollments)
    profile = build_student_profile(1, students, courses, enrollments)
    print(f"\n  Profile built with {len(profile['interests'])} interests, "
          f"{len(profile['skills_with_history'])} skills (incl. history), "
          f"{len(profile['completed_course_ids'])} completed courses")

    section("3. Rule-Based Baseline Recommendations (Top 5)")
    baseline_recs = baseline_recommend(1, students, courses, enrollments, top_n=5)
    show_recommendations("Baseline", baseline_recs)

    section("4. TF-IDF ML Recommender Recommendations (Top 5)")
    ml_recs = ml_recommend(1, students, courses, enrollments, top_n=5)
    show_recommendations("TF-IDF ML", ml_recs)

    section("5. Comparison: Baseline vs ML overlap")
    baseline_ids = {r.course_id for r in baseline_recs}
    ml_ids = {r.course_id for r in ml_recs}
    overlap = baseline_ids & ml_ids
    print(f"  Baseline IDs: {sorted(baseline_ids)}")
    print(f"  ML IDs:       {sorted(ml_ids)}")
    print(f"  Overlap:      {sorted(overlap)} ({len(overlap)} courses)")

    section("6. Multi-Student Smoke Test")
    for sid in [1, 2, 3, 7, 21]:
        recs = ml_recommend(sid, students, courses, enrollments, top_n=3)
        student_name = students.loc[students["student_id"] == sid].iloc[0]["name"]
        print(f"  Student {sid} ({student_name}): {[r.course_name for r in recs]}")

    section("7. Evaluation Summary")
    results = run_evaluation(k_values=[5, 10], hide_ratio=0.3, seed=42)
    print(format_report(results))

    section("8. Demo Complete")
    print("  Pipeline: Student ID -> Profile -> Filter -> Score -> Rank -> Top 5 -> Explanations")
    print("  All stages working. Use 'uvicorn api.main:app --reload' to serve the API.")


def main() -> None:
    run_demo()


if __name__ == "__main__":
    main()
