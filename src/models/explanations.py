from __future__ import annotations

from typing import Dict, List, Set

import pandas as pd

from src.data.preprocessing import parse_prerequisites, parse_tags

INTEREST_LABELS: Dict[str, str] = {
    "ai": "AI",
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "data science": "Data Science",
    "web development": "Web Development",
    "web": "Web",
    "cloud": "Cloud",
    "cybersecurity": "Cybersecurity",
    "security": "Security",
    "networks": "Networks",
    "networking": "Networking",
    "mobile": "Mobile",
    "mathematics": "Mathematics",
    "math": "Mathematics",
    "statistics": "Statistics",
    "algorithms": "Algorithms",
    "programming": "Programming",
    "systems": "Systems",
    "theory": "Theory",
    "databases": "Databases",
    "devops": "DevOps",
    "ui design": "UI Design",
    "design": "Design",
    "cryptography": "Cryptography",
    "nlp": "NLP",
    "deep learning": "Deep Learning",
    "computer vision": "Computer Vision",
    "big data": "Big Data",
    "data mining": "Data Mining",
    "data visualization": "Data Visualization",
    "competitive programming": "Competitive Programming",
    "ethical hacking": "Ethical Hacking",
    "operating systems": "Operating Systems",
    "distributed systems": "Distributed Systems",
    "robotics": "Robotics",
    "quantum computing": "Quantum Computing",
}


def canonical_interest(label: str) -> str:
    key = label.lower().strip()
    return INTEREST_LABELS.get(key, label)


def course_interest_tags(course_row: pd.Series) -> Set[str]:
    tags = {str(course_row.get("category", "")).lower()}
    tags.update(s.lower() for s in parse_tags(course_row.get("skills", "")))
    name = str(course_row.get("name", "")).lower()
    tags.update(name.split())
    desc = str(course_row.get("description", "")).lower()
    for keyword in INTEREST_LABELS:
        if " " in keyword:
            if keyword in name or keyword in desc:
                tags.add(keyword)
        else:
            if keyword in name.split() or keyword in desc.split():
                tags.add(keyword)
    tags.discard("")
    return tags


def interest_reasons(
    student_interests: List[str], course_row: pd.Series
) -> List[str]:
    if not student_interests:
        return []
    course_tags = course_interest_tags(course_row)
    course_text = " ".join(course_tags)
    reasons: List[str] = []
    for interest in student_interests:
        key = interest.lower().strip()
        if key in course_tags or key in course_text:
            reasons.append(f"Matches your {canonical_interest(interest)} interest")
    return reasons


def skill_reasons(
    student_skills: List[str], course_row: pd.Series
) -> List[str]:
    if not student_skills:
        return []
    course_skills = {s.lower() for s in parse_tags(course_row.get("skills", ""))}
    reasons: List[str] = []
    seen = set()
    for skill in student_skills:
        key = skill.lower().strip()
        if key in course_skills and key not in seen:
            reasons.append(f"Matches your {skill} skill")
            seen.add(key)
    return reasons


def prerequisite_reasons(
    course_row: pd.Series, completed_ids: Set[int]
) -> List[str]:
    prereqs = parse_prerequisites(course_row.get("prerequisites", ""))
    if not prereqs:
        return ["No prerequisites required"]
    satisfied = sum(1 for p in prereqs if p in completed_ids)
    if satisfied == len(prereqs):
        return ["Prerequisites completed"]
    if satisfied == 0:
        return [f"Prerequisites not yet completed ({len(prereqs)} required)"]
    return [f"Prerequisites partially completed ({satisfied}/{len(prereqs)})"]


def category_reasons(
    completed_categories: List[str], course_row: pd.Series
) -> List[str]:
    if not completed_categories:
        return []
    course_cat = str(course_row.get("category", "")).lower()
    seen = set()
    reasons: List[str] = []
    for cat in completed_categories:
        key = cat.lower().strip()
        if key == course_cat and key not in seen:
            reasons.append(f"Builds on your {course_row.get('category', '')} background")
            seen.add(key)
    return reasons


def difficulty_reasons(student_year: int, course_row: pd.Series) -> List[str]:
    difficulty = str(course_row.get("difficulty", "Intermediate"))
    name = str(course_row.get("name", ""))
    if student_year == 1 and difficulty == "Beginner":
        return [f"{name} is a beginner-friendly starting point"]
    if student_year == 4 and difficulty == "Advanced":
        return [f"{name} is an advanced course suited to your final year"]
    if student_year <= 2 and difficulty == "Advanced":
        return [f"{name} may be challenging at year {student_year}"]
    return []


def build_explanations(
    profile: Dict,
    course_row: pd.Series,
    completed_ids: Set[int],
    similarity: float | None = None,
    max_reasons: int = 5,
) -> List[str]:
    reasons: List[str] = []

    interests = profile.get("interests", [])
    skills = profile.get("skills_with_history", profile.get("skills", []))
    completed_categories = profile.get("completed_categories", [])
    year = int(profile.get("year", 3))

    reasons.extend(interest_reasons(interests, course_row))
    reasons.extend(skill_reasons(skills, course_row))
    reasons.extend(prerequisite_reasons(course_row, completed_ids))
    reasons.extend(category_reasons(completed_categories, course_row))
    reasons.extend(difficulty_reasons(year, course_row))

    if similarity is not None and similarity >= 0.5:
        reasons.append(f"Strong content similarity ({similarity:.0%}) with your profile")

    deduped: List[str] = []
    seen = set()
    for r in reasons:
        if r not in seen:
            deduped.append(r)
            seen.add(r)
        if len(deduped) >= max_reasons:
            break
    return deduped


def explain_recommendation(
    course_id: int,
    profile: Dict,
    courses: pd.DataFrame,
    completed_ids: Set[int],
    similarity: float | None = None,
) -> List[str]:
    rows = courses.loc[courses["course_id"] == course_id]
    if rows.empty:
        raise KeyError(f"course_id {course_id} not found")
    return build_explanations(profile, rows.iloc[0], completed_ids, similarity)
