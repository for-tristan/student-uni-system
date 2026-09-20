from __future__ import annotations

import pandas as pd
import pytest

from src.data.preprocessing import load_courses, load_enrollments, load_students
from src.models.baseline import (
    WEIGHT_CATEGORY,
    WEIGHT_DIFFICULTY,
    WEIGHT_INTEREST,
    WEIGHT_PREREQ,
    WEIGHT_SKILL,
    Recommendation,
    category_match_score,
    difficulty_fit_score,
    interest_match_score,
    prerequisite_match_score,
    recommend_courses,
    recommend_for_profile,
    score_course,
    skill_match_score,
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


def _find_course(courses: pd.DataFrame, course_id: int) -> pd.Series:
    rows = courses.loc[courses["course_id"] == course_id]
    assert len(rows) == 1, f"course_id {course_id} not unique/missing"
    return rows.iloc[0]


def test_weights_sum_to_one() -> None:
    total = (
        WEIGHT_INTEREST + WEIGHT_SKILL + WEIGHT_PREREQ
        + WEIGHT_CATEGORY + WEIGHT_DIFFICULTY
    )
    assert abs(total - 1.0) < 1e-9


def test_interest_match_score_full(courses) -> None:
    course = _find_course(courses, 101)
    score = interest_match_score(["AI", "Algorithms"], course)
    assert score == pytest.approx(1.0)


def test_interest_match_score_partial(courses) -> None:
    course = _find_course(courses, 101)
    score = interest_match_score(["AI", "Web Development"], course)
    assert 0.0 < score < 1.0


def test_interest_match_score_no_interests(courses) -> None:
    course = _find_course(courses, 101)
    assert interest_match_score([], course) == 0.0


def test_skill_match_score_full(courses) -> None:
    course = _find_course(courses, 101)
    score = skill_match_score(["Python", "Algorithms", "Logic"], course)
    assert score == pytest.approx(1.0)


def test_skill_match_score_partial(courses) -> None:
    course = _find_course(courses, 101)
    score = skill_match_score(["Python", "React"], course)
    assert 0.0 < score < 1.0


def test_skill_match_score_case_insensitive(courses) -> None:
    course = _find_course(courses, 101)
    assert skill_match_score(["python", "algorithms", "logic"], course) == pytest.approx(1.0)


def test_skill_match_score_no_skills(courses) -> None:
    course = _find_course(courses, 101)
    assert skill_match_score([], course) == 0.0


def test_prerequisite_match_score_no_prereqs(courses) -> None:
    course = _find_course(courses, 101)
    assert prerequisite_match_score(course, set()) == 1.0


def test_prerequisite_match_score_all_satisfied(courses) -> None:
    course = _find_course(courses, 102)
    assert prerequisite_match_score(course, {101}) == 1.0


def test_prerequisite_match_score_partial(courses) -> None:
    course = _find_course(courses, 108)
    score = prerequisite_match_score(course, {107})
    assert 0.0 < score < 1.0


def test_prerequisite_match_score_none_satisfied(courses) -> None:
    course = _find_course(courses, 102)
    assert prerequisite_match_score(course, set()) == 0.0


def test_category_match_score_match(courses) -> None:
    course = _find_course(courses, 102)
    assert category_match_score(["AI", "Data Science"], course) == pytest.approx(0.5)


def test_category_match_score_no_match(courses) -> None:
    course = _find_course(courses, 102)
    assert category_match_score(["Web", "Mobile"], course) == 0.0


def test_category_match_score_empty(courses) -> None:
    course = _find_course(courses, 102)
    assert category_match_score([], course) == 0.0


def test_difficulty_fit_score_beginner_year1(courses) -> None:
    course = _find_course(courses, 106)
    assert difficulty_fit_score(1, course) == 1.0


def test_difficulty_fit_score_advanced_year1(courses) -> None:
    course = _find_course(courses, 102)
    assert difficulty_fit_score(1, course) == 0.0


def test_difficulty_fit_score_advanced_year4(courses) -> None:
    course = _find_course(courses, 102)
    assert difficulty_fit_score(4, course) == 1.0


def test_score_course_returns_recommendation(courses) -> None:
    course = _find_course(courses, 102)
    profile = {
        "interests": ["AI", "Machine Learning"],
        "skills": ["Python", "Statistics", "Algorithms"],
        "skills_with_history": ["Python", "Statistics", "Algorithms"],
        "completed_categories": ["AI"],
        "completed_course_ids": [101],
        "year": 3,
    }
    rec = score_course(course, profile, {101})
    assert isinstance(rec, Recommendation)
    assert rec.course_id == 102
    assert rec.course_name == "Machine Learning"
    assert 0.0 <= rec.score <= 1.0
    assert isinstance(rec.reasons, list)
    assert isinstance(rec.components, dict)
    assert set(rec.components) == {"interest", "skill", "prerequisite", "category", "difficulty"}


def test_score_course_with_completed_prereqs_gives_high_score(courses) -> None:
    course = _find_course(courses, 102)
    profile = {
        "interests": ["AI"],
        "skills": ["Python", "Statistics", "Algorithms"],
        "skills_with_history": ["Python", "Statistics", "Algorithms"],
        "completed_categories": [],
        "year": 3,
    }
    rec = score_course(course, profile, {101})
    assert rec.components["prerequisite"] == 1.0
    assert rec.score > 0.5


def test_score_course_with_missing_prereqs_gives_low_score(courses) -> None:
    course = _find_course(courses, 102)
    profile = {
        "interests": ["AI"],
        "skills": ["Python"],
        "skills_with_history": ["Python"],
        "completed_categories": [],
        "year": 3,
    }
    rec = score_course(course, profile, set())
    assert rec.components["prerequisite"] == 0.0
    assert rec.score < 0.5


def test_recommend_courses_returns_top_n(students, courses, enrollments) -> None:
    recs = recommend_courses(1, students, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    assert all(isinstance(r, Recommendation) for r in recs)


def test_recommend_courses_scores_sorted_descending(students, courses, enrollments) -> None:
    recs = recommend_courses(1, students, courses, enrollments, top_n=10)
    scores = [r.score for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_recommend_courses_excludes_completed(students, courses, enrollments) -> None:
    from src.data.preprocessing import get_completed_course_ids
    completed = set(get_completed_course_ids(enrollments, 1))
    recs = recommend_courses(1, students, courses, enrollments, top_n=20)
    recommended_ids = {r.course_id for r in recs}
    assert recommended_ids.isdisjoint(completed)


def test_recommend_courses_excludes_in_progress(students, courses, enrollments) -> None:
    in_progress_ids = set(
        enrollments.loc[
            (enrollments["student_id"] == 1) & (enrollments["status"] == "in_progress"),
            "course_id",
        ].astype(int).tolist()
    )
    recs = recommend_courses(1, students, courses, enrollments, top_n=50)
    recommended_ids = {r.course_id for r in recs}
    assert recommended_ids.isdisjoint(in_progress_ids)


def test_recommend_courses_excludes_unsatisfied_prereqs(students, courses, enrollments) -> None:
    from src.data.preprocessing import get_completed_course_ids, parse_prerequisites
    completed = set(get_completed_course_ids(enrollments, 1))
    recs = recommend_courses(1, students, courses, enrollments, top_n=50)
    for rec in recs:
        course_row = courses.loc[courses["course_id"] == rec.course_id].iloc[0]
        prereqs = parse_prerequisites(course_row["prerequisites"])
        for p in prereqs:
            assert p in completed, f"Course {rec.course_id} recommended with unsatisfied prereq {p}"


def test_recommend_courses_deterministic(students, courses, enrollments) -> None:
    recs_a = recommend_courses(1, students, courses, enrollments, top_n=5)
    recs_b = recommend_courses(1, students, courses, enrollments, top_n=5)
    assert [r.course_id for r in recs_a] == [r.course_id for r in recs_b]
    assert [r.score for r in recs_a] == [r.score for r in recs_b]


def test_recommend_courses_ai_student(students, courses, enrollments) -> None:
    recs = recommend_courses(1, students, courses, enrollments, top_n=5)
    assert len(recs) > 0
    recommended_ids = {r.course_id for r in recs}
    ai_course_ids = set(
        courses.loc[courses["category"] == "AI", "course_id"].astype(int).tolist()
    )
    assert recommended_ids & ai_course_ids


def test_recommend_courses_web_student(students, courses, enrollments) -> None:
    web_student = pd.DataFrame([{
        "student_id": 9799,
        "name": "WebLearner",
        "year": 2,
        "major": "Computer Science",
        "interests": "Web Development",
        "skills": "HTML,CSS,JavaScript",
    }])
    students_ext = pd.concat([students, web_student], ignore_index=True)
    recs = recommend_courses(9799, students_ext, courses, enrollments, top_n=5)
    assert len(recs) > 0
    recommended_ids = {r.course_id for r in recs}
    web_course_ids = set(
        courses.loc[courses["category"] == "Web", "course_id"].astype(int).tolist()
    )
    assert recommended_ids & web_course_ids


def test_recommend_courses_cybersecurity_student(students, courses, enrollments) -> None:
    student_id = 3
    recs = recommend_courses(student_id, students, courses, enrollments, top_n=5)
    assert len(recs) > 0
    recommended_ids = {r.course_id for r in recs}
    sec_course_ids = set(
        courses.loc[courses["category"] == "Cybersecurity", "course_id"].astype(int).tolist()
    )
    assert recommended_ids & sec_course_ids


def test_recommend_courses_no_interests(students, courses, enrollments) -> None:
    no_interest_student = pd.DataFrame([{
        "student_id": 9999,
        "name": "NoInterests",
        "year": 2,
        "major": "Computer Science",
        "interests": "",
        "skills": "Python",
    }])
    students_ext = pd.concat([students, no_interest_student], ignore_index=True)
    recs = recommend_courses(9999, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    for r in recs:
        assert r.components["interest"] == 0.0


def test_recommend_courses_few_skills(students, courses, enrollments) -> None:
    few_skills_student = pd.DataFrame([{
        "student_id": 9998,
        "name": "FewSkills",
        "year": 1,
        "major": "Computer Science",
        "interests": "AI",
        "skills": "Python",
    }])
    students_ext = pd.concat([students, few_skills_student], ignore_index=True)
    recs = recommend_courses(9998, students_ext, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    for r in recs:
        assert r.score <= 1.0


def test_recommend_courses_unknown_student(students, courses, enrollments) -> None:
    with pytest.raises(KeyError):
        recommend_courses(99999, students, courses, enrollments, top_n=5)


def test_recommend_courses_top_n_zero(students, courses, enrollments) -> None:
    recs = recommend_courses(1, students, courses, enrollments, top_n=0)
    assert recs == []


def test_recommend_courses_relaxes_prereqs_when_disabled(students, courses, enrollments) -> None:
    from src.data.preprocessing import get_completed_course_ids, parse_prerequisites
    completed = set(get_completed_course_ids(enrollments, 1))
    recs_strict = recommend_courses(1, students, courses, enrollments, top_n=50, enforce_prereqs=True)
    recs_relaxed = recommend_courses(1, students, courses, enrollments, top_n=50, enforce_prereqs=False)
    strict_ids = {r.course_id for r in recs_strict}
    relaxed_ids = {r.course_id for r in recs_relaxed}
    assert strict_ids.issubset(relaxed_ids)
    for cid in relaxed_ids - strict_ids:
        course_row = courses.loc[courses["course_id"] == cid].iloc[0]
        prereqs = parse_prerequisites(course_row["prerequisites"])
        assert any(p not in completed for p in prereqs)


def test_recommend_for_profile(students, courses, enrollments) -> None:
    from src.data.preprocessing import build_student_profile, get_completed_course_ids
    profile = build_student_profile(1, students, courses, enrollments)
    completed = set(get_completed_course_ids(enrollments, 1))
    enrolled = set(
        enrollments.loc[enrollments["student_id"] == 1, "course_id"].astype(int).tolist()
    )
    recs = recommend_for_profile(profile, courses, completed, enrolled, top_n=5)
    assert len(recs) <= 5
    rec_ids = {r.course_id for r in recs}
    assert rec_ids.isdisjoint(enrolled)


def test_recommendation_dataclass() -> None:
    rec = Recommendation(
        course_id=101,
        course_name="Test",
        score=0.85,
        reasons=["reason1", "reason2"],
        components={"interest": 1.0},
    )
    assert rec.course_id == 101
    assert rec.course_name == "Test"
    assert rec.score == 0.85
    assert rec.reasons == ["reason1", "reason2"]
    assert rec.components == {"interest": 1.0}


def test_reasons_reference_real_features(students, courses, enrollments) -> None:
    from src.data.preprocessing import build_student_profile
    profile = build_student_profile(1, students, courses, enrollments)
    profile_skills = {s.lower() for s in profile["skills_with_history"]}
    profile_interests = {i.lower() for i in profile["interests"]}

    recs = recommend_courses(1, students, courses, enrollments, top_n=5)
    for rec in recs:
        course_row = courses.loc[courses["course_id"] == rec.course_id].iloc[0]
        course_skills = {s.lower() for s in str(course_row["skills"]).split(",") if s}
        course_category = str(course_row["category"]).lower()
        for reason in rec.reasons:
            if "interest" in reason.lower():
                matched = False
                for interest in profile_interests:
                    if interest in reason.lower():
                        matched = True
                        assert (interest in course_category) or any(
                            interest in s for s in course_skills
                        )
                assert matched
            elif "skill" in reason.lower():
                matched = False
                for skill in profile_skills:
                    if skill in reason.lower():
                        matched = True
                        assert skill in course_skills
                assert matched


def test_score_in_valid_range_for_all_students(students, courses, enrollments) -> None:
    for sid in students["student_id"].tolist():
        recs = recommend_courses(sid, students, courses, enrollments, top_n=5)
        for r in recs:
            assert 0.0 <= r.score <= 1.0
