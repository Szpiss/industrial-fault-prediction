from unittest.mock import Mock

from fastapi import Query
from sqlalchemy.exc import OperationalError

from app.db.session import get_db


def test_health_queries_database(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["database"] == "ok"
    assert response.json()["timestamp"].endswith("Z")


def test_database_failure_returns_503_without_connection_secrets(client):
    failed_session = Mock()
    failed_session.execute.side_effect = OperationalError("SECRET SQL", {}, Exception("PASSWORD"))
    client.app.dependency_overrides[get_db] = lambda: failed_session
    response = client.get("/api/v1/health")
    assert response.status_code == 503
    assert response.json() == {"error": {"code": "HTTP_503", "message": "Database is unavailable"}}


def test_openapi_and_swagger(client):
    assert "/api/v1/health" in client.get("/openapi.json").json()["paths"]
    assert client.get("/docs").status_code == 200


def test_not_found_is_consistent(client):
    assert client.get("/not-found").json()["error"]["code"] == "HTTP_404"


def test_cors_allows_development_origin(client):
    response = client.options(
        "/api/v1/health",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_rejects_unknown_origin(client):
    response = client.options(
        "/api/v1/health",
        headers={"Origin": "https://unknown.example", "Access-Control-Request-Method": "GET"},
    )
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_unexpected_errors_do_not_expose_details(client):
    @client.app.get("/test-crash", include_in_schema=False)
    def crash():
        raise RuntimeError("private information")

    assert client.get("/test-crash").json() == {
        "error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}
    }


def test_validation_error_envelope(client):
    @client.app.get("/test-validation", include_in_schema=False)
    def validate(limit: int = Query()):
        return {"limit": limit}

    response = client.get("/test-validation", params={"limit": "invalid"})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"
