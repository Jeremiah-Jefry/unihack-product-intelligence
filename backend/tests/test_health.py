"""Tests for the health endpoint."""

from datetime import datetime

from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for GET /api/v1/health."""

    def test_health_returns_200(self, client: TestClient):
        response = client.get("/api/v1/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client: TestClient):
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_returns_service_name(self, client: TestClient):
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["service"] == "product-intelligence-api"

    def test_health_returns_version(self, client: TestClient):
        response = client.get("/api/v1/health")
        data = response.json()
        assert data["version"] == "0.1.0"

    def test_health_returns_valid_timestamp(self, client: TestClient):
        response = client.get("/api/v1/health")
        data = response.json()
        assert "timestamp" in data
        ts = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
        assert isinstance(ts, datetime)

    def test_health_response_structure(self, client: TestClient):
        response = client.get("/api/v1/health")
        data = response.json()
        required_keys = {"status", "service", "version", "timestamp"}
        assert set(data.keys()) == required_keys

    def test_health_does_not_expose_secrets(self, client: TestClient):
        response = client.get("/api/v1/health")
        body = response.text.lower()
        for term in ["openai", "password", "secret", "credential", "api_key"]:
            assert term not in body, f"Sensitive term '{term}' found in health response"
