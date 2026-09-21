from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.data.preprocessing import (
    build_student_profile,
    build_student_profile_text,
    filter_available_courses,
    filter_prereq_satisfied,
    get_completed_course_ids,
    normalize_text,
    parse_tags,
)

DEFAULT_TFIDF_PARAMS: Dict = {
    "lowercase": True,
    "stop_words": "english",
    "ngram_range": (1, 2),
    "min_df": 1,
    "max_df": 0.95,
    "sublinear_tf": True,
}


@dataclass
class MLRecommendation:
    course_id: int
    course_name: str
    score: float
    reasons: List[str] = field(default_factory=list)
    similarity: float = 0.0


class TfidfCourseRecommender:
    def __init__(self, courses: pd.DataFrame, tfidf_params: Dict | None = None) -> None:
        self.courses = courses.copy().reset_index(drop=True)
        self.params: Dict = {**DEFAULT_TFIDF_PARAMS, **(tfidf_params or {})}
        self._course_texts: List[str] = []
        self._tfidf_matrix = None
        self._vectorizer: TfidfVectorizer | None = None
        self._fit()

    def _build_course_text(self, course_row: pd.Series) -> str:
        parts = [
            str(course_row.get("name", "")),
            str(course_row.get("category", "")),
            str(course_row.get("description", "")),
            str(course_row.get("skills", "")),
        ]
        return " ".join(p for p in parts if p)

    def _fit(self) -> None:
        self._course_texts = [
            self._build_course_text(row) for _, row in self.courses.iterrows()
        ]
        self._vectorizer = TfidfVectorizer(**self.params)
        self._tfidf_matrix = self._vectorizer.fit_transform(self._course_texts)

    def get_course_text(self, course_id: int) -> str:
        rows = self.courses.loc[self.courses["course_id"] == course_id]
        if rows.empty:
            raise KeyError(f"course_id {course_id} not found")
        idx = rows.index[0]
        return self._course_texts[idx]

    def get_course_index(self, course_id: int) -> int:
        rows = self.courses.loc[self.courses["course_id"] == course_id]
        if rows.empty:
            raise KeyError(f"course_id {course_id} not found")
        return rows.index[0]

    def vectorize_text(self, text: str) -> np.ndarray:
        if self._vectorizer is None:
            raise RuntimeError("Recommender not fitted")
        return self._vectorizer.transform([text])

    def build_student_vector(self, profile: Dict) -> np.ndarray:
        text = build_student_profile_text(profile)
        return self.vectorize_text(text)

    def compute_similarities(self, profile: Dict) -> np.ndarray:
        student_vec = self.build_student_vector(profile)
        sims = cosine_similarity(student_vec, self._tfidf_matrix).flatten()
        return sims

    def recommend(
        self,
        student_id: int,
        students: pd.DataFrame,
        enrollments: pd.DataFrame,
        top_n: int = 5,
        enforce_prereqs: bool = True,
        min_similarity: float = 0.0,
    ) -> List[MLRecommendation]:
        profile = build_student_profile(student_id, students, self.courses, enrollments)
        completed_ids = set(get_completed_course_ids(enrollments, student_id))
        available = filter_available_courses(student_id, self.courses, enrollments)
        if enforce_prereqs:
            available = filter_prereq_satisfied(available, completed_ids)

        sims = self.compute_similarities(profile)

        results: List[MLRecommendation] = []
        for _, row in available.iterrows():
            idx = row.name
            sim = float(sims[idx])
            if sim < min_similarity:
                continue
            reasons = self._build_reasons(profile, row, completed_ids, sim)
            results.append(MLRecommendation(
                course_id=int(row["course_id"]),
                course_name=str(row["name"]),
                score=round(sim, 4),
                similarity=round(sim, 4),
                reasons=reasons,
            ))

        results.sort(key=lambda r: (-r.score, r.course_id))
        return results[:top_n]

    def recommend_for_profile(
        self,
        profile: Dict,
        completed_ids: Set[int],
        enrolled_ids: Set[int] | None = None,
        top_n: int = 5,
        enforce_prereqs: bool = True,
        min_similarity: float = 0.0,
    ) -> List[MLRecommendation]:
        enrolled_ids = enrolled_ids or set()
        available = self.courses.loc[~self.courses["course_id"].isin(enrolled_ids)].copy()
        if enforce_prereqs:
            available = filter_prereq_satisfied(available, completed_ids)

        sims = self.compute_similarities(profile)

        results: List[MLRecommendation] = []
        for _, row in available.iterrows():
            idx = row.name
            sim = float(sims[idx])
            if sim < min_similarity:
                continue
            reasons = self._build_reasons(profile, row, completed_ids, sim)
            results.append(MLRecommendation(
                course_id=int(row["course_id"]),
                course_name=str(row["name"]),
                score=round(sim, 4),
                similarity=round(sim, 4),
                reasons=reasons,
            ))

        results.sort(key=lambda r: (-r.score, r.course_id))
        return results[:top_n]

    def _build_reasons(
        self,
        profile: Dict,
        course_row: pd.Series,
        completed_ids: Set[int],
        similarity: float,
    ) -> List[str]:
        from src.models.explanations import build_explanations
        return build_explanations(
            profile, course_row, completed_ids, similarity=similarity, max_reasons=5
        )


def recommend_courses(
    student_id: int,
    students: pd.DataFrame,
    courses: pd.DataFrame,
    enrollments: pd.DataFrame,
    top_n: int = 5,
    enforce_prereqs: bool = True,
) -> List[MLRecommendation]:
    rec = TfidfCourseRecommender(courses)
    return rec.recommend(
        student_id, students, enrollments,
        top_n=top_n, enforce_prereqs=enforce_prereqs,
    )
