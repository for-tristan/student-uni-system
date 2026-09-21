from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from typing import List

import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.data.preprocessing import load_courses, load_enrollments, load_students
from src.models.recommender import TfidfCourseRecommender, MLRecommendation


class RecommendationItem(BaseModel):
    course_id: int
    course_name: str
    score: float
    reasons: List[str] = Field(default_factory=list)
    similarity: float | None = None


class RecommendationResponse(BaseModel):
    student_id: int
    recommender: str
    top_n: int
    recommendations: List[RecommendationItem]


class HealthResponse(BaseModel):
    status: str
    students: int
    courses: int
    enrollments: int


class RootResponse(BaseModel):
    name: str
    version: str
    endpoints: List[str]


class _AppState:
    students: pd.DataFrame
    courses: pd.DataFrame
    enrollments: pd.DataFrame
    recommender: TfidfCourseRecommender


_state = _AppState()


def load_data() -> None:
    _state.students = load_students()
    _state.courses = load_courses()
    _state.enrollments = load_enrollments()
    _state.recommender = TfidfCourseRecommender(_state.courses)


def get_state() -> _AppState:
    if not hasattr(_state, "students") or _state.students is None:
        load_data()
    return _state


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        load_data()
        yield

    app = FastAPI(
        title="University Course Recommendation System",
        description="Content-based course recommender exposing Top-N recommendations per student.",
        version="1.0.0",
        lifespan=lifespan,
    )

    @app.get("/", response_model=RootResponse, tags=["meta"])
    def root() -> RootResponse:
        return RootResponse(
            name="University Course Recommendation System",
            version="1.0.0",
            endpoints=[
                "GET /",
                "GET /health",
                "GET /recommendations/{student_id}",
            ],
        )

    @app.get("/health", response_model=HealthResponse, tags=["meta"])
    def health() -> HealthResponse:
        state = get_state()
        return HealthResponse(
            status="ok",
            students=len(state.students),
            courses=len(state.courses),
            enrollments=len(state.enrollments),
        )

    @app.get(
        "/recommendations/{student_id}",
        response_model=RecommendationResponse,
        tags=["recommendations"],
    )
    def get_recommendations(
        student_id: int,
        top_n: int = Query(default=5, ge=1, le=20),
        enforce_prereqs: bool = Query(default=True),
    ) -> RecommendationResponse:
        state = get_state()
        if student_id not in set(state.students["student_id"]):
            raise HTTPException(
                status_code=404,
                detail=f"Student with id {student_id} not found",
            )

        try:
            recs: List[MLRecommendation] = state.recommender.recommend(
                student_id,
                state.students,
                state.enrollments,
                top_n=top_n,
                enforce_prereqs=enforce_prereqs,
            )
        except KeyError:
            raise HTTPException(
                status_code=404,
                detail=f"Student with id {student_id} not found in profile builder",
            )

        items: List[RecommendationItem] = []
        for r in recs:
            items.append(RecommendationItem(
                course_id=r.course_id,
                course_name=r.course_name,
                score=r.score,
                reasons=r.reasons,
                similarity=r.similarity,
            ))

        return RecommendationResponse(
            student_id=student_id,
            recommender="tfidf",
            top_n=top_n,
            recommendations=items,
        )

    return app


app = create_app()
