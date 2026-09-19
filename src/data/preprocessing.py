from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Set

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
STUDENTS_CSV = DATA_DIR / "students.csv"
COURSES_CSV = DATA_DIR / "courses.csv"
ENROLLMENTS_CSV = DATA_DIR / "enrollments.csv"

VALID_STATUSES = {"completed", "failed", "in_progress", "dropped"}
VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}


def load_students(path: Path | str = STUDENTS_CSV) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"student_id", "name", "year", "major", "interests", "skills"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"students.csv missing columns: {missing}")
    df["student_id"] = df["student_id"].astype(int)
    df["year"] = df["year"].astype(int)
    df["name"] = df["name"].fillna("").astype(str)
    df["major"] = df["major"].fillna("").astype(str)
    df["interests"] = df["interests"].fillna("").astype(str)
    df["skills"] = df["skills"].fillna("").astype(str)
    return df


def load_courses(path: Path | str = COURSES_CSV) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {
        "course_id", "name", "category", "description",
        "skills", "prerequisites", "difficulty", "credits",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"courses.csv missing columns: {missing}")
    df["course_id"] = df["course_id"].astype(int)
    df["credits"] = df["credits"].astype(int)
    for col in ("name", "category", "description", "skills", "prerequisites", "difficulty"):
        df[col] = df[col].fillna("").astype(str)
    return df


def load_enrollments(path: Path | str = ENROLLMENTS_CSV) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"student_id", "course_id", "grade", "status"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"enrollments.csv missing columns: {missing}")
    df["student_id"] = df["student_id"].astype(int)
    df["course_id"] = df["course_id"].astype(int)
    df["status"] = df["status"].fillna("").astype(str)
    df["grade"] = pd.to_numeric(df["grade"], errors="coerce")
    return df


def parse_tags(value: str | float | None) -> List[str]:
    if value is None:
        return []
    if isinstance(value, float) and pd.isna(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    return [t.strip() for t in text.split(",") if t.strip()]


def parse_prerequisites(value: str | float | None) -> List[int]:
    tags = parse_tags(value)
    result: List[int] = []
    for tag in tags:
        try:
            result.append(int(tag))
        except ValueError:
            continue
    return result


def normalize_text(value: str | float | None) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    text = str(value).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_completed_course_ids(enrollments: pd.DataFrame, student_id: int) -> List[int]:
    mask = (enrollments["student_id"] == student_id) & (enrollments["status"] == "completed")
    return enrollments.loc[mask, "course_id"].astype(int).tolist()


def get_completed_course_ids_by_status(
    enrollments: pd.DataFrame, student_id: int, statuses: Set[str]
) -> List[int]:
    mask = (enrollments["student_id"] == student_id) & (enrollments["status"].isin(statuses))
    return enrollments.loc[mask, "course_id"].astype(int).tolist()


def build_student_profile(
    student_id: int,
    students: pd.DataFrame,
    courses: pd.DataFrame,
    enrollments: pd.DataFrame,
) -> Dict:
    student_rows = students.loc[students["student_id"] == student_id]
    if student_rows.empty:
        raise KeyError(f"Student {student_id} not found")
    student = student_rows.iloc[0]

    interests = parse_tags(student["interests"])
    skills = parse_tags(student["skills"])

    completed_ids = set(get_completed_course_ids(enrollments, student_id))

    completed_courses = courses.loc[courses["course_id"].isin(completed_ids)]

    completed_categories: List[str] = []
    completed_skills: List[str] = []
    completed_names: List[str] = []
    for _, row in completed_courses.iterrows():
        completed_names.append(str(row["name"]))
        completed_categories.append(str(row["category"]))
        completed_skills.extend(parse_tags(row["skills"]))

    return {
        "student_id": int(student_id),
        "name": str(student["name"]),
        "year": int(student["year"]),
        "major": str(student["major"]),
        "interests": interests,
        "skills": skills,
        "completed_course_ids": sorted(completed_ids),
        "completed_course_names": completed_names,
        "completed_categories": completed_categories,
        "completed_skills": list(dict.fromkeys(completed_skills)),
        "skills_with_history": list(dict.fromkeys(skills + completed_skills)),
    }


def filter_available_courses(
    student_id: int,
    courses: pd.DataFrame,
    enrollments: pd.DataFrame,
) -> pd.DataFrame:
    enrolled_ids = set(
        enrollments.loc[enrollments["student_id"] == student_id, "course_id"].astype(int).tolist()
    )
    return courses.loc[~courses["course_id"].isin(enrolled_ids)].copy()


def filter_prereq_satisfied(
    courses: pd.DataFrame,
    completed_ids: Set[int],
) -> pd.DataFrame:
    def _satisfied(prereq_str: str) -> bool:
        prereqs = parse_prerequisites(prereq_str)
        if not prereqs:
            return True
        return all(p in completed_ids for p in prereqs)

    mask = courses["prerequisites"].apply(_satisfied)
    return courses.loc[mask].copy()


def build_course_text(course_row: pd.Series) -> str:
    parts = [
        str(course_row.get("name", "")),
        str(course_row.get("category", "")),
        str(course_row.get("description", "")),
        str(course_row.get("skills", "")),
    ]
    return " ".join(p for p in parts if p)


def build_student_profile_text(profile: Dict) -> str:
    parts = [
        " ".join(profile.get("interests", [])),
        " ".join(profile.get("skills_with_history", [])),
        " ".join(profile.get("completed_categories", [])),
        " ".join(profile.get("completed_course_names", [])),
    ]
    return " ".join(p for p in parts if p)


def validate_data(
    students: pd.DataFrame,
    courses: pd.DataFrame,
    enrollments: pd.DataFrame,
) -> List[str]:
    errors: List[str] = []

    if students["student_id"].duplicated().any():
        errors.append("Duplicate student_id values found")
    if courses["course_id"].duplicated().any():
        errors.append("Duplicate course_id values found")

    valid_student_ids = set(students["student_id"])
    bad_students = set(enrollments["student_id"]) - valid_student_ids
    if bad_students:
        errors.append(f"Enrollments reference unknown student_ids: {sorted(bad_students)}")

    valid_course_ids = set(courses["course_id"])
    bad_courses = set(enrollments["course_id"]) - valid_course_ids
    if bad_courses:
        errors.append(f"Enrollments reference unknown course_ids: {sorted(bad_courses)}")

    bad_statuses = set(enrollments["status"].unique()) - VALID_STATUSES - {""}
    if bad_statuses:
        errors.append(f"Unknown enrollment statuses: {bad_statuses}")

    bad_difficulties = set(courses["difficulty"].unique()) - VALID_DIFFICULTIES - {""}
    if bad_difficulties:
        errors.append(f"Unknown difficulties: {bad_difficulties}")

    for _, row in courses.iterrows():
        prereqs = parse_prerequisites(row["prerequisites"])
        if row["course_id"] in prereqs:
            errors.append(f"Course {row['course_id']} lists itself as a prerequisite")
        for p in prereqs:
            if p not in valid_course_ids:
                errors.append(f"Course {row['course_id']} has unknown prerequisite {p}")

    dups = enrollments.duplicated(subset=["student_id", "course_id"])
    if dups.any():
        errors.append(f"{int(dups.sum())} duplicate (student_id, course_id) pairs")

    return errors
