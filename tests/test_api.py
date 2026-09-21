from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.main import app, load_data


@pytest.fixture(scope="module")
def client() -> TestClient:
    load_data()
    with TestClient(app) as c:
        yield c


def test_root_endpoint(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert "endpoints" in data
    assert isinstance(data["endpoints"], list)
    assert len(data["endpoints"]) >= 3


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["students"] > 0
    assert data["courses"] > 0
    assert data["enrollments"] > 0


def test_recommendations_valid_student(client: TestClient) -> None:
    response = client.get("/recommendations/1")
    assert response.status_code == 200
    data = response.json()
    assert data["student_id"] == 1
    assert data["recommender"] == "tfidf"
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) <= 5


def test_recommendations_structure(client: TestClient) -> None:
    response = client.get("/recommendations/1")
    data = response.json()
    for item in data["recommendations"]:
        assert "course_id" in item
        assert "course_name" in item
        assert "score" in item
        assert "reasons" in item
        assert isinstance(item["course_id"], int)
        assert isinstance(item["course_name"], str)
        assert isinstance(item["score"], (int, float))
        assert isinstance(item["reasons"], list)
        assert 0.0 <= item["score"] <= 1.0


def test_recommendations_invalid_student(client: TestClient) -> None:
    response = client.get("/recommendations/99999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "99999" in data["detail"]


def test_recommendations_top_n_param(client: TestClient) -> None:
    response = client.get("/recommendations/1?top_n=3")
    assert response.status_code == 200
    data = response.json()
    assert data["top_n"] == 3
    assert len(data["recommendations"]) <= 3


def test_recommendations_top_n_invalid_too_large(client: TestClient) -> None:
    response = client.get("/recommendations/1?top_n=100")
    assert response.status_code == 422


def test_recommendations_top_n_invalid_zero(client: TestClient) -> None:
    response = client.get("/recommendations/1?top_n=0")
    assert response.status_code == 422


def test_recommendations_top_n_invalid_negative(client: TestClient) -> None:
    response = client.get("/recommendations/1?top_n=-5")
    assert response.status_code == 422


def test_recommendations_enforce_prereqs_param(client: TestClient) -> None:
    response = client.get("/recommendations/1?enforce_prereqs=false")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["recommendations"], list)


def test_recommendations_scores_sorted_descending(client: TestClient) -> None:
    response = client.get("/recommendations/1?top_n=10")
    data = response.json()
    scores = [item["score"] for item in data["recommendations"]]
    assert scores == sorted(scores, reverse=True)


def test_recommendations_excludes_completed(client: TestClient) -> None:
    from src.data.preprocessing import get_completed_course_ids, load_enrollments
    enrollments = load_enrollments()
    completed = set(get_completed_course_ids(enrollments, 1))
    response = client.get("/recommendations/1?top_n=20")
    data = response.json()
    rec_ids = {item["course_id"] for item in data["recommendations"]}
    assert rec_ids.isdisjoint(completed)


def test_recommendations_reasons_non_empty(client: TestClient) -> None:
    response = client.get("/recommendations/1")
    data = response.json()
    for item in data["recommendations"]:
        assert len(item["reasons"]) > 0


def test_recommendations_all_students(client: TestClient) -> None:
    from src.data.preprocessing import load_students
    students = load_students()
    for sid in students["student_id"].tolist():
        response = client.get(f"/recommendations/{sid}?top_n=3")
        assert response.status_code == 200


def test_unknown_route_returns_404(client: TestClient) -> None:
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_recommendations_student_id_must_be_int(client: TestClient) -> None:
    response = client.get("/recommendations/abc")
    assert response.status_code == 422


def test_openapi_schema_available(client: TestClient) -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "University Course Recommendation System"
