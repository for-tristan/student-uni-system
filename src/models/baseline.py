from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set

import pandas as pd

from src.data.preprocessing import (
    build_student_profile,
    filter_available_courses,
    filter_prereq_satisfied,
    get_completed_course_ids,
    parse_prerequisites,
    parse_tags,
)

WEIGHT_INTEREST = 0.30
WEIGHT_SKILL = 0.30
WEIGHT_PREREQ = 0.20
WEIGHT_CATEGORY = 0.10
WEIGHT_DIFFICULTY = 0.10

DIFFICULTY_ORDER = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
YEAR_TO_DIFFICULTY = {
    1: {"Beginner": 1.0, "Intermediate": 0.5, "Advanced": 0.0},
    2: {"Beginner": 0.8, "Intermediate": 1.0, "Advanced": 0.4},
    3: {"Beginner": 0.6, "Intermediate": 1.0, "Advanced": 0.8},
    4: {"Beginner": 0.4, "Intermediate": 0.8, "Advanced": 1.0},
    5: {"Beginner": 0.3, "Intermediate": 0.7, "Advanced": 1.0},
}


@dataclass
class Recommendation:
    course_id: int
    course_name: str
    score: float
    reasons: List[str] = field(default_factory=list)
    components: Dict[str, float] = field(default_factory=dict)


def interest_match_score(student_interests: List[str], course_row: pd.Series) -> float:
    if not student_interests:
        return 0.0
    course_tags = {str(course_row.get("category", ""))}
    course_tags.update(parse_tags(course_row.get("skills", "")))
    course_tags.discard("")
    course_text = " ".join(course_tags).lower()
    matched = 0
    for interest in student_interests:
        if interest.lower() in course_text:
            matched += 1
    return matched / len(student_interests)


def skill_match_score(student_skills: List[str], course_row: pd.Series) -> float:
    if not student_skills:
        return 0.0
    course_skills = set(parse_tags(course_row.get("skills", "")))
    if not course_skills:
        return 0.0
    student_skills_set = {s.lower() for s in student_skills}
    course_skills_set = {s.lower() for s in course_skills}
    matched = len(student_skills_set & course_skills_set)
    return matched / len(course_skills_set)


def prerequisite_match_score(
    course_row: pd.Series, completed_ids: Set[int]
) -> float:
    prereqs = parse_prerequisites(course_row.get("prerequisites", ""))
    if not prereqs:
        return 1.0
    satisfied = sum(1 for p in prereqs if p in completed_ids)
    return satisfied / len(prereqs)


def category_match_score(
    student_categories: List[str], course_row: pd.Series
) -> float:
    if not student_categories:
        return 0.0
    course_cat = str(course_row.get("category", "")).lower()
    matched = sum(1 for c in student_categories if c.lower() == course_cat)
    return min(matched / len(student_categories), 1.0)


def difficulty_fit_score(student_year: int, course_row: pd.Series) -> float:
    difficulty = str(course_row.get("difficulty", "Intermediate"))
    table = YEAR_TO_DIFFICULTY.get(student_year, YEAR_TO_DIFFICULTY[3])
    return table.get(difficulty, 0.5)


def build_reasons(
    student_interests: List[str],
    student_skills: List[str],
    course_row: pd.Series,
    completed_ids: Set[int],
    components: Dict[str, float],
) -> List[str]:
    reasons: List[str] = []

    course_skills_lower = {s.lower() for s in parse_tags(course_row.get("skills", ""))}
    for interest in student_interests:
        course_tags = {str(course_row.get("category", "")).lower()}
        course_tags.update(parse_tags(course_row.get("skills", "")))
        course_tags_lower = {t.lower() for t in course_tags if t}
        if interest.lower() in course_tags_lower:
            reasons.append(f"Matches your {interest} interest")

    for skill in student_skills:
        if skill.lower() in course_skills_lower:
            reasons.append(f"Matches your {skill} skill")

    prereqs = parse_prerequisites(course_row.get("prerequisites", ""))
    if prereqs and components.get("prerequisite", 0.0) >= 1.0:
        reasons.append("Prerequisites completed")
    elif not prereqs:
        reasons.append("No prerequisites required")

    return reasons


def score_course(
    course_row: pd.Series,
    profile: Dict,
    completed_ids: Set[int],
) -> Recommendation:
    interests = profile.get("interests", [])
    skills = profile.get("skills_with_history", profile.get("skills", []))
    completed_categories = profile.get("completed_categories", [])
    year = int(profile.get("year", 3))

    i_score = interest_match_score(interests, course_row)
    s_score = skill_match_score(skills, course_row)
    p_score = prerequisite_match_score(course_row, completed_ids)
    c_score = category_match_score(completed_categories, course_row)
    d_score = difficulty_fit_score(year, course_row)

    components = {
        "interest": i_score,
        "skill": s_score,
        "prerequisite": p_score,
        "category": c_score,
        "difficulty": d_score,
    }

    final = (
        WEIGHT_INTEREST * i_score
        + WEIGHT_SKILL * s_score
        + WEIGHT_PREREQ * p_score
        + WEIGHT_CATEGORY * c_score
        + WEIGHT_DIFFICULTY * d_score
    )

    reasons = build_reasons(interests, skills, course_row, completed_ids, components)

    return Recommendation(
        course_id=int(course_row["course_id"]),
        course_name=str(course_row["name"]),
        score=round(final, 4),
        reasons=reasons,
        components={k: round(v, 4) for k, v in components.items()},
    )


def recommend_courses(
    student_id: int,
    students: pd.DataFrame,
    courses: pd.DataFrame,
    enrollments: pd.DataFrame,
    top_n: int = 5,
    enforce_prereqs: bool = True,
    min_score: float = 0.0,
) -> List[Recommendation]:
    profile = build_student_profile(student_id, students, courses, enrollments)
    completed_ids = set(get_completed_course_ids(enrollments, student_id))

    available = filter_available_courses(student_id, courses, enrollments)

    if enforce_prereqs:
        available = filter_prereq_satisfied(available, completed_ids)

    scored: List[Recommendation] = []
    for _, row in available.iterrows():
        rec = score_course(row, profile, completed_ids)
        if rec.score >= min_score:
            scored.append(rec)

    scored.sort(key=lambda r: (-r.score, r.course_id))

    return scored[:top_n]


def recommend_for_profile(
    profile: Dict,
    courses: pd.DataFrame,
    completed_ids: Set[int],
    enrolled_ids: Set[int] | None = None,
    top_n: int = 5,
    enforce_prereqs: bool = True,
) -> List[Recommendation]:
    enrolled_ids = enrolled_ids or set()
    available = courses.loc[~courses["course_id"].isin(enrolled_ids)].copy()

    if enforce_prereqs:
        available = filter_prereq_satisfied(available, completed_ids)

    scored: List[Recommendation] = []
    for _, row in available.iterrows():
        scored.append(score_course(row, profile, completed_ids))

    scored.sort(key=lambda r: (-r.score, r.course_id))
    return scored[:top_n]
