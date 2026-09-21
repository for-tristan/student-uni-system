from __future__ import annotations

import pandas as pd
import pytest

from src.data.preprocessing import (
    build_student_profile,
    get_completed_course_ids,
    load_courses,
    load_enrollments,
    load_students,
    parse_tags,
)
from src.models.baseline import recommend_courses as baseline_recs
from src.models.recommender import recommend_courses as ml_recs


@pytest.fixture(scope="module")
def students() -> pd.DataFrame:
    return load_students()


@pytest.fixture(scope="module")
def courses() -> pd.DataFrame:
    return load_courses()


@pytest.fixture(scope="module")
def enrollments() -> pd.DataFrame:
    return load_enrollments()


def _make_student(sid: int, interests: str, skills: str, year: int = 3) -> pd.DataFrame:
    return pd.DataFrame([{
        "student_id": sid,
        "name": f"TestStudent{sid}",
        "year": year,
        "major": "Computer Science",
        "interests": interests,
        "skills": skills,
    }])


def test_student_with_no_interests(students, courses, enrollments) -> None:
    new_student = _make_student(9001, "", "Python")
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9001, students_ext, courses, enrollments, top_n=5)
    assert isinstance(recs, list)
    assert len(recs) <= 5
    for r in recs:
        assert r.components["interest"] == 0.0


def test_student_with_no_skills(students, courses, enrollments) -> None:
    new_student = _make_student(9002, "AI", "")
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9002, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    for r in recs:
        assert r.components["skill"] == 0.0


def test_student_with_no_interests_and_no_skills(students, courses, enrollments) -> None:
    new_student = _make_student(9003, "", "")
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9003, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    for r in recs:
        assert r.score < 1.0


def test_student_with_one_skill(students, courses, enrollments) -> None:
    new_student = _make_student(9004, "AI", "Python")
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9004, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    assert all(0.0 <= r.score <= 1.0 for r in recs)


def test_student_with_many_skills(students, courses, enrollments) -> None:
    new_student = _make_student(
        9005, "AI",
        "Python,Statistics,Algorithms,Linear Algebra,Machine Learning,SQL,Linux,Networking"
    )
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9005, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    if recs:
        assert recs[0].score > 0.3


def test_student_year1_only_gets_beginner_friendly(students, courses, enrollments) -> None:
    new_student = _make_student(9006, "Programming", "Python", year=1)
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9006, students_ext, courses, enrollments, top_n=10)
    for r in recs:
        course_row = courses.loc[courses["course_id"] == r.course_id].iloc[0]
        assert course_row["difficulty"] != "Advanced"


def test_student_year4_gets_advanced_options(students, courses, enrollments) -> None:
    new_student = _make_student(9007, "AI", "Python,Machine Learning,Statistics", year=4)
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = baseline_recs(9007, students_ext, courses, enrollments, top_n=10)
    difficulties = [
        courses.loc[courses["course_id"] == r.course_id].iloc[0]["difficulty"]
        for r in recs
    ]
    if len(recs) >= 3:
        assert "Advanced" in difficulties or "Intermediate" in difficulties


def test_student_who_completed_everything(students, courses, enrollments) -> None:
    new_student = _make_student(9008, "AI", "Python", year=4)
    students_ext = pd.concat([students, new_student], ignore_index=True)
    all_course_ids = set(courses["course_id"].astype(int).tolist())
    new_enrollments = pd.DataFrame([
        {"student_id": 9008, "course_id": cid, "grade": 90, "status": "completed"}
        for cid in all_course_ids
    ])
    enrollments_ext = pd.concat([enrollments, new_enrollments], ignore_index=True)
    recs = baseline_recs(9008, students_ext, courses, enrollments_ext, top_n=5)
    assert recs == []


def test_student_with_all_failed_courses(students, courses, enrollments) -> None:
    new_student = _make_student(9009, "AI", "Python", year=3)
    students_ext = pd.concat([students, new_student], ignore_index=True)
    new_enrollments = pd.DataFrame([
        {"student_id": 9009, "course_id": 101, "grade": 30, "status": "failed"},
    ])
    enrollments_ext = pd.concat([enrollments, new_enrollments], ignore_index=True)
    recs = baseline_recs(9009, students_ext, courses, enrollments_ext, top_n=5)
    rec_ids = {r.course_id for r in recs}
    assert 101 not in rec_ids
    assert len(recs) <= 5


def test_student_with_dropped_courses(students, courses, enrollments) -> None:
    new_student = _make_student(9010, "AI", "Python", year=3)
    students_ext = pd.concat([students, new_student], ignore_index=True)
    new_enrollments = pd.DataFrame([
        {"student_id": 9010, "course_id": 101, "grade": None, "status": "dropped"},
    ])
    enrollments_ext = pd.concat([enrollments, new_enrollments], ignore_index=True)
    recs = baseline_recs(9010, students_ext, courses, enrollments_ext, top_n=10)
    assert 101 not in {r.course_id for r in recs}


def test_ml_recommender_handles_no_interests(students, courses, enrollments) -> None:
    new_student = _make_student(9011, "", "Python")
    students_ext = pd.concat([students, new_student], ignore_index=True)
    recs = ml_recs(9011, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    for r in recs:
        assert 0.0 <= r.score <= 1.0


def test_ml_recommender_handles_unknown_student(students, courses, enrollments) -> None:
    with pytest.raises(KeyError):
        ml_recs(99999, students, courses, enrollments, top_n=5)


def test_baseline_consistency_across_calls(students, courses, enrollments) -> None:
    for sid in [1, 2, 3]:
        r1 = baseline_recs(sid, students, courses, enrollments, top_n=5)
        r2 = baseline_recs(sid, students, courses, enrollments, top_n=5)
        assert [r.course_id for r in r1] == [r.course_id for r in r2]


def test_ml_consistency_across_calls(students, courses, enrollments) -> None:
    for sid in [1, 2, 3]:
        r1 = ml_recs(sid, students, courses, enrollments, top_n=5)
        r2 = ml_recs(sid, students, courses, enrollments, top_n=5)
        assert [r.course_id for r in r1] == [r.course_id for r in r2]


def test_top_n_bounds(students, courses, enrollments) -> None:
    recs = baseline_recs(1, students, courses, enrollments, top_n=1)
    assert len(recs) <= 1


def test_top_n_large(students, courses, enrollments) -> None:
    recs = baseline_recs(1, students, courses, enrollments, top_n=100)
    assert len(recs) <= len(courses)


def test_completed_course_ids_correctness(students, courses, enrollments) -> None:
    completed = get_completed_course_ids(enrollments, 1)
    expected = enrollments.loc[
        (enrollments["student_id"] == 1) & (enrollments["status"] == "completed"),
        "course_id",
    ].astype(int).tolist()
    assert set(completed) == set(expected)


def test_parse_tags_with_extra_commas() -> None:
    assert parse_tags("Python,,SQL,") == ["Python", "SQL"]


def test_parse_tags_with_only_commas() -> None:
    assert parse_tags(",,,") == []


def test_parse_tags_with_whitespace_only() -> None:
    assert parse_tags("  ,  ,  ") == []


def test_build_student_profile_includes_history(students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    assert set(profile["skills"]).issubset(set(profile["skills_with_history"]))
    if profile["completed_course_ids"]:
        assert len(profile["skills_with_history"]) >= len(profile["skills"])
