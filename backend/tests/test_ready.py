"""Tests for the readiness endpoint."""

from datetime import datetime
from unittest.mock import MagicMock

from fastapi.testclient import TestClient


class TestReadinessEndpoint:
    """Tests for GET /api/v1/ready."""

    def test_ready_returns_200_when_db_available(self, client: TestClient):
        response = client.get("/api/v1/ready")
        assert response.status_code == 200

    def test_ready_returns_ready_status(self, client: TestClient):
        response = client.get("/api/v1/ready")
        data = response.json()
        assert data["status"] == "ready"

    def test_ready_returns_database_ok(self, client: TestClient):
        response = client.get("/api/v1/ready")
        data = response.json()
        assert data["database"] == "ok"

    def test_ready_returns_valid_timestamp(self, client: TestClient):
        response = client.get("/api/v1/ready")
        data = response.json()
        assert "timestamp" in data
        ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        assert isinstance(ts, datetime)

    def test_ready_response_structure(self, client: TestClient):
        response = client.get("/api/v1/ready")
        data = response.json()
        required_keys = {"status", "database", "timestamp"}
        assert set(data.keys()) == required_keys

    def test_ready_returns_503_when_db_unavailable(self, client: TestClient):
        """When the database query fails, readiness should return 503."""

        def failing_execute(*args, **kwargs):
            raise Exception("Database connection refused")

        # Override with a mock session that fails on execute
        from app.core.database import get_db
        from app.main import app

        mock_session = MagicMock()
        mock_session.execute.side_effect = Exception("Database connection refused")

        def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        try:
            response = client.get("/api/v1/ready")
            assert response.status_code == 503
            data = response.json()
            assert data["status"] == "not_ready"
            assert data["database"] == "unavailable"
        finally:
            app.dependency_overrides.clear()

    def test_health_still_works_when_db_unavailable(self, client: TestClient):
        """Liveness (health) should work even when readiness (DB) fails."""
        from app.core.database import get_db
        from app.main import app

        mock_session = MagicMock()
        mock_session.execute.side_effect = Exception("Database connection refused")

        def override_get_db():
            yield mock_session

        app.dependency_overrides[get_db] = override_get_db
        try:
            health_response = client.get("/api/v1/health")
            assert health_response.status_code == 200
            assert health_response.json()["status"] == "ok"
        finally:
            app.dependency_overrides.clear()
