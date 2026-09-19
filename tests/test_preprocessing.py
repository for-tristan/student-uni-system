from __future__ import annotations

import pandas as pd
import pytest

from src.data.preprocessing import (
    build_course_text,
    build_student_profile,
    build_student_profile_text,
    filter_available_courses,
    filter_prereq_satisfied,
    get_completed_course_ids,
    get_completed_course_ids_by_status,
    load_courses,
    load_enrollments,
    load_students,
    normalize_text,
    parse_prerequisites,
    parse_tags,
    validate_data,
)


@pytest.fixture(scope="module")
def students() -> pd.DataFrame:
    return load_students()


@pytest.fixture(scope="module")
def courses() -> pd.DataFrame:
    return load_courses()


@pytest.fixture(scope="module")
def enrollments() -> pd.DataFrame:
    return load_enrollments()


def test_load_students_returns_dataframe(students: pd.DataFrame) -> None:
    assert isinstance(students, pd.DataFrame)
    assert len(students) > 0
    expected_cols = {"student_id", "name", "year", "major", "interests", "skills"}
    assert set(students.columns) == expected_cols


def test_load_courses_returns_dataframe(courses: pd.DataFrame) -> None:
    assert isinstance(courses, pd.DataFrame)
    assert len(courses) > 0
    expected_cols = {
        "course_id", "name", "category", "description",
        "skills", "prerequisites", "difficulty", "credits",
    }
    assert set(courses.columns) == expected_cols


def test_load_enrollments_returns_dataframe(enrollments: pd.DataFrame) -> None:
    assert isinstance(enrollments, pd.DataFrame)
    assert len(enrollments) > 0
    expected_cols = {"student_id", "course_id", "grade", "status"}
    assert set(enrollments.columns) == expected_cols


def test_load_students_fills_missing_with_empty_string() -> None:
    df = pd.DataFrame({
        "student_id": [999],
        "name": ["Test"],
        "year": [1],
        "major": ["CS"],
        "interests": [None],
        "skills": [""],
    })
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        df.to_csv(f, index=False)
        path = f.name
    try:
        loaded = load_students(path)
        assert loaded.loc[0, "interests"] == ""
        assert loaded.loc[0, "skills"] == ""
    finally:
        os.unlink(path)


def test_parse_tags_basic() -> None:
    assert parse_tags("Python,SQL,Algorithms") == ["Python", "SQL", "Algorithms"]


def test_parse_tags_with_spaces() -> None:
    assert parse_tags(" Python , SQL , Algorithms ") == ["Python", "SQL", "Algorithms"]


def test_parse_tags_empty() -> None:
    assert parse_tags("") == []


def test_parse_tags_none() -> None:
    assert parse_tags(None) == []


def test_parse_tags_nan() -> None:
    assert parse_tags(float("nan")) == []


def test_parse_prerequisites_single() -> None:
    assert parse_prerequisites("101") == [101]


def test_parse_prerequisites_multiple() -> None:
    assert parse_prerequisites("101,102,103") == [101, 102, 103]


def test_parse_prerequisites_ignores_non_numeric() -> None:
    assert parse_prerequisites("101,abc,102") == [101, 102]


def test_parse_prerequisites_empty() -> None:
    assert parse_prerequisites("") == []


def test_normalize_text_lowercases() -> None:
    assert normalize_text("Machine Learning") == "machine learning"


def test_normalize_text_removes_punctuation() -> None:
    assert normalize_text("AI, ML & Data!") == "ai ml data"


def test_normalize_text_collapses_whitespace() -> None:
    assert normalize_text("hello    world") == "hello world"


def test_normalize_text_empty() -> None:
    assert normalize_text("") == ""


def test_normalize_text_nan() -> None:
    assert normalize_text(float("nan")) == ""


def test_get_completed_course_ids(enrollments: pd.DataFrame) -> None:
    completed = get_completed_course_ids(enrollments, 1)
    assert isinstance(completed, list)
    assert len(completed) > 0
    assert all(isinstance(c, int) for c in completed)
    assert all(c > 0 for c in completed)


def test_get_completed_course_ids_excludes_in_progress(enrollments: pd.DataFrame) -> None:
    completed = set(get_completed_course_ids(enrollments, 1))
    in_progress = set(
        get_completed_course_ids_by_status(enrollments, 1, {"in_progress"})
    )
    assert completed.isdisjoint(in_progress)


def test_get_completed_course_ids_unknown_student(enrollments: pd.DataFrame) -> None:
    assert get_completed_course_ids(enrollments, 99999) == []


def test_build_student_profile(students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    assert profile["student_id"] == 1
    assert isinstance(profile["name"], str)
    assert profile["year"] >= 1
    assert isinstance(profile["interests"], list)
    assert isinstance(profile["skills"], list)
    assert isinstance(profile["completed_course_ids"], list)
    assert all(isinstance(c, int) for c in profile["completed_course_ids"])
    assert isinstance(profile["completed_course_names"], list)
    assert isinstance(profile["completed_categories"], list)
    assert isinstance(profile["completed_skills"], list)
    assert isinstance(profile["skills_with_history"], list)
    assert set(profile["skills"]).issubset(set(profile["skills_with_history"]))


def test_build_student_profile_unknown_student(students, courses, enrollments) -> None:
    with pytest.raises(KeyError):
        build_student_profile(99999, students, courses, enrollments)


def test_build_student_profile_no_completed(
    students, courses, enrollments
) -> None:
    sid = int(students.iloc[-1]["student_id"]) + 1
    new_student = pd.DataFrame([{
        "student_id": sid,
        "name": "Ghost",
        "year": 1,
        "major": "CS",
        "interests": "AI",
        "skills": "Python",
    }])
    students_ext = pd.concat([students, new_student], ignore_index=True)
    profile = build_student_profile(sid, students_ext, courses, enrollments)
    assert profile["completed_course_ids"] == []
    assert profile["completed_course_names"] == []
    assert profile["completed_categories"] == []
    assert profile["completed_skills"] == []
    assert profile["skills_with_history"] == profile["skills"]


def test_filter_available_courses_excludes_enrolled(
    students, courses, enrollments
) -> None:
    enrolled = set(
        enrollments.loc[enrollments["student_id"] == 1, "course_id"].astype(int).tolist()
    )
    available = filter_available_courses(1, courses, enrollments)
    assert set(available["course_id"]).isdisjoint(enrolled)
    assert len(available) <= len(courses)


def test_filter_available_courses_unknown_student(courses, enrollments) -> None:
    available = filter_available_courses(99999, courses, enrollments)
    assert len(available) == len(courses)


def test_filter_prereq_satisfied_no_prereqs(courses) -> None:
    completed = set()
    filtered = filter_prereq_satisfied(courses, completed)
    no_prereq = courses.loc[courses["prerequisites"] == ""]
    assert set(filtered["course_id"]) == set(no_prereq["course_id"])


def test_filter_prereq_satisfied_with_completed(courses) -> None:
    no_prereq_ids = set(
        courses.loc[courses["prerequisites"] == "", "course_id"].tolist()
    )
    filtered = filter_prereq_satisfied(courses, no_prereq_ids)

    expected = set(no_prereq_ids)
    for _, row in courses.iterrows():
        prereqs = parse_prerequisites(row["prerequisites"])
        if prereqs and all(p in no_prereq_ids for p in prereqs):
            expected.add(int(row["course_id"]))

    assert set(filtered["course_id"]) == expected
    assert len(filtered) >= len(no_prereq_ids)


def test_filter_prereq_satisfied_all_courses(courses) -> None:
    all_ids = set(courses["course_id"].tolist())
    filtered = filter_prereq_satisfied(courses, all_ids)
    assert len(filtered) == len(courses)


def test_build_course_text_contains_key_fields(courses) -> None:
    course = courses.iloc[0]
    text = build_course_text(course)
    assert str(course["name"]) in text
    assert str(course["category"]) in text
    assert str(course["description"]) in text
    assert str(course["skills"]) in text


def test_build_student_profile_text_contains_interests_and_skills(
    students, courses, enrollments
) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    text = build_student_profile_text(profile)
    for interest in profile["interests"]:
        assert interest in text
    for skill in profile["skills"]:
        assert skill in text


def test_validate_data_returns_no_errors(students, courses, enrollments) -> None:
    errors = validate_data(students, courses, enrollments)
    assert errors == []


def test_validate_data_detects_duplicate_students(courses, enrollments) -> None:
    students_dup = pd.concat([
        pd.read_csv("data/students.csv"),
        pd.read_csv("data/students.csv").head(1),
    ], ignore_index=True)
    errors = validate_data(students_dup, courses, enrollments)
    assert any("Duplicate student_id" in e for e in errors)


def test_validate_data_detects_unknown_status(students, courses) -> None:
    bad_enr = pd.read_csv("data/enrollments.csv").copy()
    bad_enr.loc[0, "status"] = "weird"
    errors = validate_data(students, courses, bad_enr)
    assert any("Unknown enrollment statuses" in e for e in errors)
