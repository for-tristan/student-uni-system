from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from src.data.preprocessing import (
    build_student_profile,
    get_completed_course_ids,
    load_courses,
    load_enrollments,
    load_students,
)
from src.models.recommender import (
    MLRecommendation,
    TfidfCourseRecommender,
    DEFAULT_TFIDF_PARAMS,
    recommend_courses,
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


@pytest.fixture(scope="module")
def recommender(courses: pd.DataFrame) -> TfidfCourseRecommender:
    return TfidfCourseRecommender(courses)


def test_default_tfidf_params_present() -> None:
    assert "ngram_range" in DEFAULT_TFIDF_PARAMS
    assert "stop_words" in DEFAULT_TFIDF_PARAMS


def test_recommender_initialization(recommender: TfidfCourseRecommender) -> None:
    assert recommender._vectorizer is not None
    assert recommender._tfidf_matrix is not None
    assert recommender._tfidf_matrix.shape[0] > 0
    assert recommender._tfidf_matrix.shape[1] > 0


def test_recommender_matrix_matches_courses(
    recommender: TfidfCourseRecommender, courses: pd.DataFrame
) -> None:
    assert recommender._tfidf_matrix.shape[0] == len(courses)


def test_get_course_text(recommender: TfidfCourseRecommender) -> None:
    text = recommender.get_course_text(102)
    assert "Machine Learning" in text
    assert "AI" in text


def test_get_course_text_unknown(recommender: TfidfCourseRecommender) -> None:
    with pytest.raises(KeyError):
        recommender.get_course_text(99999)


def test_get_course_index(recommender: TfidfCourseRecommender) -> None:
    idx = recommender.get_course_index(101)
    assert int(idx) >= 0


def test_vectorize_text_returns_sparse(recommender: TfidfCourseRecommender) -> None:
    vec = recommender.vectorize_text("python machine learning")
    assert vec.shape[0] == 1


def test_compute_similarities_shape(recommender: TfidfCourseRecommender, students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    sims = recommender.compute_similarities(profile)
    assert sims.shape == (len(courses),)
    assert (sims >= 0).all()
    assert (sims <= 1.0 + 1e-9).all()


def test_recommend_returns_top_n(recommender, students, courses, enrollments) -> None:
    recs = recommender.recommend(1, students, enrollments, top_n=5)
    assert len(recs) <= 5
    assert all(isinstance(r, MLRecommendation) for r in recs)


def test_recommend_scores_sorted_descending(recommender, students, courses, enrollments) -> None:
    recs = recommender.recommend(1, students, enrollments, top_n=10)
    scores = [r.score for r in recs]
    assert scores == sorted(scores, reverse=True)


def test_recommend_scores_in_range(recommender, students, courses, enrollments) -> None:
    for sid in students["student_id"].tolist()[:5]:
        recs = recommender.recommend(sid, students, enrollments, top_n=5)
        for r in recs:
            assert 0.0 <= r.score <= 1.0


def test_recommend_excludes_completed(recommender, students, courses, enrollments) -> None:
    completed = set(get_completed_course_ids(enrollments, 1))
    recs = recommender.recommend(1, students, enrollments, top_n=50)
    rec_ids = {r.course_id for r in recs}
    assert rec_ids.isdisjoint(completed)


def test_recommend_excludes_in_progress(recommender, students, courses, enrollments) -> None:
    in_progress = set(
        enrollments.loc[
            (enrollments["student_id"] == 1) & (enrollments["status"] == "in_progress"),
            "course_id",
        ].astype(int).tolist()
    )
    recs = recommender.recommend(1, students, enrollments, top_n=50)
    rec_ids = {r.course_id for r in recs}
    assert rec_ids.isdisjoint(in_progress)


def test_recommend_enforces_prereqs(recommender, students, courses, enrollments) -> None:
    from src.data.preprocessing import parse_prerequisites
    completed = set(get_completed_course_ids(enrollments, 1))
    recs = recommender.recommend(1, students, enrollments, top_n=50, enforce_prereqs=True)
    for r in recs:
        row = courses.loc[courses["course_id"] == r.course_id].iloc[0]
        prereqs = parse_prerequisites(row["prerequisites"])
        for p in prereqs:
            assert p in completed


def test_recommend_relaxes_prereqs(recommender, students, courses, enrollments) -> None:
    strict = recommender.recommend(1, students, enrollments, top_n=50, enforce_prereqs=True)
    relaxed = recommender.recommend(1, students, enrollments, top_n=50, enforce_prereqs=False)
    strict_ids = {r.course_id for r in strict}
    relaxed_ids = {r.course_id for r in relaxed}
    assert strict_ids.issubset(relaxed_ids)


def test_recommend_deterministic(recommender, students, courses, enrollments) -> None:
    a = recommender.recommend(1, students, enrollments, top_n=5)
    b = recommender.recommend(1, students, enrollments, top_n=5)
    assert [r.course_id for r in a] == [r.course_id for r in b]
    assert [r.score for r in a] == [r.score for r in b]


def test_recommend_ai_student_gets_ai_courses(recommender, students, courses, enrollments) -> None:
    recs = recommender.recommend(1, students, enrollments, top_n=5)
    rec_ids = {r.course_id for r in recs}
    ai_ids = set(courses.loc[courses["category"] == "AI", "course_id"].astype(int).tolist())
    assert rec_ids & ai_ids


def test_recommend_web_student_gets_web_courses(recommender, students, courses, enrollments) -> None:
    web_student = pd.DataFrame([{
        "student_id": 9799,
        "name": "WebLearner",
        "year": 2,
        "major": "Computer Science",
        "interests": "Web Development",
        "skills": "HTML,CSS,JavaScript",
    }])
    students_ext = pd.concat([students, web_student], ignore_index=True)
    recs = recommender.recommend(9799, students_ext, enrollments, top_n=5)
    rec_ids = {r.course_id for r in recs}
    web_ids = set(courses.loc[courses["category"] == "Web", "course_id"].astype(int).tolist())
    assert rec_ids & web_ids


def test_recommend_cybersecurity_student(recommender, students, courses, enrollments) -> None:
    recs = recommender.recommend(3, students, enrollments, top_n=5)
    rec_ids = {r.course_id for r in recs}
    sec_ids = set(courses.loc[courses["category"] == "Cybersecurity", "course_id"].astype(int).tolist())
    assert rec_ids & sec_ids


def test_recommend_unknown_student(recommender, students, courses, enrollments) -> None:
    with pytest.raises(KeyError):
        recommender.recommend(99999, students, enrollments, top_n=5)


def test_recommend_for_profile(recommender, students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    completed = set(get_completed_course_ids(enrollments, 1))
    enrolled = set(enrollments.loc[enrollments["student_id"] == 1, "course_id"].astype(int).tolist())
    recs = recommender.recommend_for_profile(profile, completed, enrolled, top_n=5)
    assert len(recs) <= 5
    rec_ids = {r.course_id for r in recs}
    assert rec_ids.isdisjoint(enrolled)


def test_min_similarity_filter(recommender, students, courses, enrollments) -> None:
    recs_low = recommender.recommend(1, students, enrollments, top_n=50, min_similarity=0.0)
    recs_high = recommender.recommend(1, students, enrollments, top_n=50, min_similarity=0.5)
    assert len(recs_high) <= len(recs_low)
    for r in recs_high:
        assert r.score >= 0.5


def test_module_level_recommend_courses(students, courses, enrollments) -> None:
    recs = recommend_courses(1, students, courses, enrollments, top_n=5)
    assert len(recs) <= 5
    assert all(isinstance(r, MLRecommendation) for r in recs)


def test_reasons_present(recommender, students, courses, enrollments) -> None:
    recs = recommender.recommend(1, students, enrollments, top_n=5)
    for r in recs:
        assert isinstance(r.reasons, list)


def test_recommend_top_n_zero(recommender, students, courses, enrollments) -> None:
    assert recommender.recommend(1, students, enrollments, top_n=0) == []


def test_student_vector_uses_history(recommender, students, courses, enrollments) -> None:
    profile = build_student_profile(1, students, courses, enrollments)
    vec = recommender.build_student_vector(profile)
    assert vec.shape[0] == 1


def test_ml_vs_baseline_overlaps_on_ai_student(students, courses, enrollments) -> None:
    from src.models.baseline import recommend_courses as baseline_recs
    ml_recs = recommend_courses(1, students, courses, enrollments, top_n=5)
    base_recs = baseline_recs(1, students, courses, enrollments, top_n=5)
    ml_ids = {r.course_id for r in ml_recs}
    base_ids = {r.course_id for r in base_recs}
    assert len(ml_ids & base_ids) >= 1
