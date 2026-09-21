from __future__ import annotations

import pandas as pd
import pytest

from src.data.preprocessing import (
    build_student_profile,
    load_courses,
    load_enrollments,
    load_students,
)
from src.models.baseline import recommend_courses as baseline_recs
from src.models.explanations import (
    build_explanations,
    canonical_interest,
    category_reasons,
    course_interest_tags,
    difficulty_reasons,
    explain_recommendation,
    interest_reasons,
    prerequisite_reasons,
    skill_reasons,
)
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


def _course(courses: pd.DataFrame, course_id: int) -> pd.Series:
    return courses.loc[courses["course_id"] == course_id].iloc[0]


def test_canonical_interest_known() -> None:
    assert canonical_interest("ai") == "AI"
    assert canonical_interest("machine learning") == "Machine Learning"
    assert canonical_interest("ml") == "Machine Learning"


def test_canonical_interest_passthrough() -> None:
    assert canonical_interest("Quantum Computing") == "Quantum Computing"


def test_course_interest_tags_includes_category(courses) -> None:
    tags = course_interest_tags(_course(courses, 102))
    assert "ai" in tags


def test_course_interest_tags_includes_skills(courses) -> None:
    tags = course_interest_tags(_course(courses, 102))
    assert "python" in tags
    assert "statistics" in tags


def test_course_interest_tags_finds_description_keywords(courses) -> None:
    tags = course_interest_tags(_course(courses, 105))
    assert any("language" in t or "nlp" in t for t in tags) or "ai" in tags


def test_interest_reasons_match(courses) -> None:
    reasons = interest_reasons(["AI", "Machine Learning"], _course(courses, 102))
    assert any("AI interest" in r for r in reasons)
    assert any("Machine Learning interest" in r for r in reasons)


def test_interest_reasons_no_match(courses) -> None:
    reasons = interest_reasons(["Web Development"], _course(courses, 102))
    assert reasons == []


def test_interest_reasons_empty_interests(courses) -> None:
    assert interest_reasons([], _course(courses, 102)) == []


def test_skill_reasons_match(courses) -> None:
    reasons = skill_reasons(["Python", "React"], _course(courses, 102))
    assert any("Python skill" in r for r in reasons)
    assert not any("React skill" in r for r in reasons)


def test_skill_reasons_deduplicated(courses) -> None:
    reasons = skill_reasons(["Python", "python", "PYTHON"], _course(courses, 102))
    assert len([r for r in reasons if "Python skill" in r]) == 1


def test_skill_reasons_empty(courses) -> None:
    assert skill_reasons([], _course(courses, 102)) == []


def test_prerequisite_reasons_no_prereqs(courses) -> None:
    reasons = prerequisite_reasons(_course(courses, 101), set())
    assert reasons == ["No prerequisites required"]


def test_prerequisite_reasons_all_satisfied(courses) -> None:
    reasons = prerequisite_reasons(_course(courses, 102), {101})
    assert reasons == ["Prerequisites completed"]


def test_prerequisite_reasons_partial(courses) -> None:
    reasons = prerequisite_reasons(_course(courses, 108), {107})
    assert any("partially" in r.lower() for r in reasons)
    assert "1/2" in reasons[0]


def test_prerequisite_reasons_none_satisfied(courses) -> None:
    reasons = prerequisite_reasons(_course(courses, 102), set())
    assert any("not yet" in r.lower() for r in reasons)


def test_category_reasons_match(courses) -> None:
    reasons = category_reasons(["AI", "Data Science"], _course(courses, 102))
    assert any("AI background" in r for r in reasons)


def test_category_reasons_no_match(courses) -> None:
    assert category_reasons(["Web", "Mobile"], _course(courses, 102)) == []


def test_category_reasons_empty(courses) -> None:
    assert category_reasons([], _course(courses, 102)) == []


def test_difficulty_reasons_beginner_year1(courses) -> None:
    reasons = difficulty_reasons(1, _course(courses, 106))
    assert any("beginner-friendly" in r for r in reasons)


def test_difficulty_reasons_advanced_year4(courses) -> None:
    reasons = difficulty_reasons(4, _course(courses, 102))
    assert any("advanced course" in r for r in reasons)


def test_difficulty_reasons_challenging(courses) -> None:
    reasons = difficulty_reasons(1, _course(courses, 102))
    assert any("challenging" in r for r in reasons)


def test_difficulty_reasons_neutral(courses) -> None:
    reasons = difficulty_reasons(3, _course(courses, 121))
    assert reasons == []


def test_build_explanations_combines_all_layers(courses) -> None:
    profile = {
        "interests": ["AI", "Machine Learning"],
        "skills": ["Python", "Statistics"],
        "skills_with_history": ["Python", "Statistics"],
        "completed_categories": ["AI"],
        "completed_course_ids": [101],
        "year": 3,
    }
    reasons = build_explanations(profile, _course(courses, 102), {101})
    assert isinstance(reasons, list)
    assert len(reasons) > 0
    assert any("interest" in r for r in reasons)
    assert any("skill" in r for r in reasons)
    assert any("Prerequisites" in r for r in reasons)


def test_build_explanations_deduplicates(courses) -> None:
    profile = {
        "interests": ["AI", "ai", "AI"],
        "skills": ["Python"],
        "skills_with_history": ["Python"],
        "completed_categories": [],
        "year": 3,
    }
    reasons = build_explanations(profile, _course(courses, 101), set())
    assert len(reasons) == len(set(reasons))


def test_build_explanations_max_reasons(courses) -> None:
    profile = {
        "interests": ["AI", "Machine Learning", "Data Science"],
        "skills": ["Python", "Statistics", "Algorithms"],
        "skills_with_history": ["Python", "Statistics", "Algorithms"],
        "completed_categories": ["AI"],
        "year": 3,
    }
    reasons = build_explanations(profile, _course(courses, 102), {101}, max_reasons=3)
    assert len(reasons) <= 3


def test_build_explanations_with_similarity(courses) -> None:
    profile = {
        "interests": ["AI"],
        "skills": ["Python"],
        "skills_with_history": ["Python"],
        "completed_categories": [],
        "year": 3,
    }
    reasons = build_explanations(profile, _course(courses, 102), {101}, similarity=0.75)
    assert any("content similarity" in r.lower() for r in reasons)


def test_build_explanations_no_similarity_threshold(courses) -> None:
    profile = {
        "interests": ["AI"],
        "skills": ["Python"],
        "skills_with_history": ["Python"],
        "completed_categories": [],
        "year": 3,
    }
    reasons = build_explanations(profile, _course(courses, 102), {101}, similarity=0.2)
    assert not any("content similarity" in r.lower() for r in reasons)


def test_explain_recommendation(courses) -> None:
    profile = {
        "interests": ["AI"],
        "skills": ["Python"],
        "skills_with_history": ["Python"],
        "completed_categories": [],
        "year": 3,
    }
    reasons = explain_recommendation(102, profile, courses, {101})
    assert isinstance(reasons, list)
    assert len(reasons) > 0


def test_explain_recommendation_unknown_course(courses) -> None:
    profile = {"interests": [], "skills": [], "skills_with_history": [],
               "completed_categories": [], "year": 3}
    with pytest.raises(KeyError):
        explain_recommendation(99999, profile, courses, set())


def test_baseline_reasons_are_data_driven(students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    recs = baseline_recs(1, students, courses, enrollments, top_n=5)
    profile_skills = {s.lower() for s in profile["skills_with_history"]}
    profile_interests = {i.lower() for i in profile["interests"]}
    for r in recs:
        course_row = _course(courses, r.course_id)
        course_skills = {s.lower() for s in str(course_row["skills"]).split(",") if s}
        course_category = str(course_row["category"]).lower()
        for reason in r.reasons:
            if "interest" in reason.lower():
                assert any(i in reason.lower() for i in profile_interests)
                assert any(
                    i in course_category or i in course_skills
                    for i in profile_interests
                )
            elif "skill" in reason.lower():
                assert any(s in reason.lower() for s in profile_skills)
                assert any(s in course_skills for s in profile_skills)


def test_ml_reasons_are_data_driven(students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    recs = ml_recs(1, students, courses, enrollments, top_n=5)
    profile_skills = {s.lower() for s in profile["skills_with_history"]}
    profile_interests = {i.lower() for i in profile["interests"]}
    for r in recs:
        course_row = _course(courses, r.course_id)
        course_skills = {s.lower() for s in str(course_row["skills"]).split(",") if s}
        course_category = str(course_row["category"]).lower()
        for reason in r.reasons:
            if "interest" in reason.lower():
                assert any(i in reason.lower() for i in profile_interests)
                assert any(
                    i in course_category or i in course_skills
                    for i in profile_interests
                )
            elif "skill" in reason.lower():
                assert any(s in reason.lower() for s in profile_skills)
                assert any(s in course_skills for s in profile_skills)


def test_reasons_no_fake_explanations(students, courses, enrollments) -> None:
    recs = baseline_recs(1, students, courses, enrollments, top_n=5)
    allowed_prefixes = (
        "Matches your", "Prerequisites", "No prerequisites",
        "Builds on your", "is a beginner", "is an advanced",
        "may be challenging", "Strong content similarity",
    )
    for r in recs:
        for reason in r.reasons:
            assert reason.startswith(allowed_prefixes), f"Unexpected reason: {reason}"


def test_reasons_include_prereq_status(students, courses, enrollments) -> None:
    recs = baseline_recs(1, students, courses, enrollments, top_n=5)
    for r in recs:
        assert any(
            "Prerequisites" in reason or "No prerequisites" in reason
            for reason in r.reasons
        ), f"Missing prerequisite info for course {r.course_id}"
