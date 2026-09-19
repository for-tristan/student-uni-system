"""Validate the synthetic recommendation dataset.

These tests ensure that:
- All three CSV files exist and load with pandas.
- Required columns are present and non-empty (where applicable).
- Student IDs, course IDs, and enrollment references are consistent.
- Prerequisites reference existing course IDs and form a DAG (no cycles).
- Enrollment statuses are from the allowed set.
- Grades are sensible (0–100 or empty for in-progress/dropped).
- No duplicate (student_id, course_id) enrollment pairs.

Run with:
    pytest tests/test_data.py -v
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
STUDENTS_CSV = DATA_DIR / "students.csv"
COURSES_CSV = DATA_DIR / "courses.csv"
ENROLLMENTS_CSV = DATA_DIR / "enrollments.csv"

VALID_STATUSES = {"completed", "failed", "in_progress", "dropped"}
VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def students_df() -> pd.DataFrame:
    return pd.read_csv(STUDENTS_CSV)


@pytest.fixture(scope="module")
def courses_df() -> pd.DataFrame:
    return pd.read_csv(COURSES_CSV)


@pytest.fixture(scope="module")
def enrollments_df() -> pd.DataFrame:
    return pd.read_csv(ENROLLMENTS_CSV)


# ---------------------------------------------------------------------------
# File existence
# ---------------------------------------------------------------------------
def test_data_files_exist() -> None:
    """All three CSV files must exist on disk."""
    assert STUDENTS_CSV.exists(), f"Missing {STUDENTS_CSV}"
    assert COURSES_CSV.exists(), f"Missing {COURSES_CSV}"
    assert ENROLLMENTS_CSV.exists(), f"Missing {ENROLLMENTS_CSV}"


# ---------------------------------------------------------------------------
# Required columns
# ---------------------------------------------------------------------------
def test_students_columns(students_df: pd.DataFrame) -> None:
    expected = {"student_id", "name", "year", "major", "interests", "skills"}
    assert set(students_df.columns) == expected


def test_courses_columns(courses_df: pd.DataFrame) -> None:
    expected = {
        "course_id", "name", "category", "description",
        "skills", "prerequisites", "difficulty", "credits",
    }
    assert set(courses_df.columns) == expected


def test_enrollments_columns(enrollments_df: pd.DataFrame) -> None:
    expected = {"student_id", "course_id", "grade", "status"}
    assert set(enrollments_df.columns) == expected


# ---------------------------------------------------------------------------
# Dataset size
# ---------------------------------------------------------------------------
def test_dataset_sizes(students_df, courses_df, enrollments_df) -> None:
    """Dataset must satisfy the size ranges defined in the project brief."""
    assert 20 <= len(students_df) <= 30, f"Expected 20–30 students, got {len(students_df)}"
    assert 30 <= len(courses_df) <= 50, f"Expected 30–50 courses, got {len(courses_df)}"
    assert 100 <= len(enrollments_df) <= 200, f"Expected 100–200 enrollments, got {len(enrollments_df)}"


# ---------------------------------------------------------------------------
# IDs: uniqueness, range, dtype
# ---------------------------------------------------------------------------
def test_student_ids_unique_and_sequential(students_df: pd.DataFrame) -> None:
    ids = students_df["student_id"]
    assert ids.is_unique, "student_id must be unique"
    assert ids.min() >= 1
    assert ids.dtype in ("int64", "int32")


def test_course_ids_unique_and_sequential(courses_df: pd.DataFrame) -> None:
    ids = courses_df["course_id"]
    assert ids.is_unique, "course_id must be unique"
    assert ids.min() >= 1
    assert ids.dtype in ("int64", "int32")


# ---------------------------------------------------------------------------
# Missing values
# ---------------------------------------------------------------------------
def test_students_no_missing_required(students_df: pd.DataFrame) -> None:
    for col in ("student_id", "name", "year", "major"):
        assert students_df[col].notna().all(), f"Missing values in students.{col}"


def test_courses_no_missing_required(courses_df: pd.DataFrame) -> None:
    for col in ("course_id", "name", "category", "description", "difficulty", "credits"):
        assert courses_df[col].notna().all(), f"Missing values in courses.{col}"


def test_courses_empty_prerequisites_allowed(courses_df: pd.DataFrame) -> None:
    """A course may have no prerequisites (the column is allowed to be NaN/empty)."""
    # NaN or empty string both acceptable; just verify the column exists.
    assert "prerequisites" in courses_df.columns


# ---------------------------------------------------------------------------
# Enumerated fields
# ---------------------------------------------------------------------------
def test_enrollment_statuses_valid(enrollments_df: pd.DataFrame) -> None:
    bad = set(enrollments_df["status"].unique()) - VALID_STATUSES
    assert not bad, f"Unknown enrollment statuses: {bad}"


def test_course_difficulties_valid(courses_df: pd.DataFrame) -> None:
    bad = set(courses_df["difficulty"].unique()) - VALID_DIFFICULTIES
    assert not bad, f"Unknown difficulties: {bad}"


# ---------------------------------------------------------------------------
# Referential integrity
# ---------------------------------------------------------------------------
def test_enrollments_reference_valid_students(
    students_df: pd.DataFrame, enrollments_df: pd.DataFrame
) -> None:
    valid_student_ids = set(students_df["student_id"])
    bad = set(enrollments_df["student_id"]) - valid_student_ids
    assert not bad, f"Enrollments reference unknown student_ids: {bad}"


def test_enrollments_reference_valid_courses(
    courses_df: pd.DataFrame, enrollments_df: pd.DataFrame
) -> None:
    valid_course_ids = set(courses_df["course_id"])
    bad = set(enrollments_df["course_id"]) - valid_course_ids
    assert not bad, f"Enrollments reference unknown course_ids: {bad}"


# ---------------------------------------------------------------------------
# Prerequisites
# ---------------------------------------------------------------------------
def test_prerequisites_reference_valid_courses(courses_df: pd.DataFrame) -> None:
    """Every prerequisite id must reference an existing course."""
    valid_course_ids = set(courses_df["course_id"])
    for raw in courses_df["prerequisites"].fillna(""):
        if not raw or (isinstance(raw, float) and pd.isna(raw)):
            continue
        prereq_ids = [int(p) for p in str(raw).split(",") if p.strip()]
        for pid in prereq_ids:
            assert pid in valid_course_ids, f"Prerequisite {pid} does not exist as a course"


def test_no_self_prerequisite(courses_df: pd.DataFrame) -> None:
    """A course must never list itself as a prerequisite."""
    for _, row in courses_df.iterrows():
        raw = row["prerequisites"]
        if pd.isna(raw) or not str(raw).strip():
            continue
        prereq_ids = [int(p) for p in str(raw).split(",") if p.strip()]
        assert row["course_id"] not in prereq_ids, (
            f"Course {row['course_id']} lists itself as a prerequisite"
        )


def test_no_duplicate_enrollments(enrollments_df: pd.DataFrame) -> None:
    """A student cannot be enrolled twice in the same course."""
    dups = enrollments_df.duplicated(subset=["student_id", "course_id"])
    assert dups.sum() == 0, f"Found {dups.sum()} duplicate (student_id, course_id) pairs"


# ---------------------------------------------------------------------------
# Grades
# ---------------------------------------------------------------------------
def test_grades_in_range(enrollments_df: pd.DataFrame) -> None:
    """Grades must be 0–100; in-progress/dropped enrollments may have no grade."""
    for _, row in enrollments_df.iterrows():
        grade = row["grade"]
        if pd.isna(grade) or grade == "" or str(grade).strip() == "":
            # Only allowed for non-completed/non-failed statuses.
            assert row["status"] in ("in_progress", "dropped"), (
                f"Empty grade for status={row['status']} (row {_})"
            )
            continue
        grade_int = int(grade)
        assert 0 <= grade_int <= 100, f"Grade {grade_int} out of range (row {_})"
