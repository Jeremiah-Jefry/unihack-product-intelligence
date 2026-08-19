"""Tests for API error handling."""

from fastapi.testclient import TestClient

from app.core.exceptions import AppError, DependencyError, NotFoundError, ValidationError
from app.main import app


class TestErrorHandling:
    """Tests for custom exception handlers and error responses."""

    def test_404_for_nonexistent_endpoint(self, client: TestClient):
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_404_for_nonexistent_endpoint_body(self, client: TestClient):
        response = client.get("/api/v1/nonexistent")
        data = response.json()
        # FastAPI default 404 returns {"detail": "Not Found"}
        assert "detail" in data or "error" in data

    def test_not_found_error_returns_404(self, client: TestClient):
        """Custom NotFoundError should map to 404."""

        @app.get("/test/not-found")
        async def raise_not_found():
            raise NotFoundError("Resource not found")

        try:
            response = client.get("/test/not-found")
            assert response.status_code == 404
            data = response.json()
            assert data["error"] == "not_found"
            assert data["message"] == "Resource not found"
        finally:
            # Clean up the test route
            app.routes.pop()

    def test_validation_error_returns_422(self, client: TestClient):
        """Custom ValidationError should map to 422."""

        @app.get("/test/validation-error")
        async def raise_validation():
            raise ValidationError("Invalid input")

        try:
            response = client.get("/test/validation-error")
            assert response.status_code == 422
            data = response.json()
            assert data["error"] == "validation_error"
            assert data["message"] == "Invalid input"
        finally:
            app.routes.pop()

    def test_dependency_error_returns_503(self, client: TestClient):
        """Custom DependencyError should map to 503."""

        @app.get("/test/dep-error")
        async def raise_dep():
            raise DependencyError("Service unavailable")

        try:
            response = client.get("/test/dep-error")
            assert response.status_code == 503
            data = response.json()
            assert data["error"] == "dependency_unavailable"
            assert data["message"] == "Service unavailable"
        finally:
            app.routes.pop()

    def test_generic_app_error_returns_500(self, client: TestClient):
        """Generic AppError should map to 500."""

        @app.get("/test/app-error")
        async def raise_app():
            raise AppError("Something went wrong")

        try:
            response = client.get("/test/app-error")
            assert response.status_code == 500
            data = response.json()
            assert data["error"] == "internal_error"
            assert data["message"] == "Something went wrong"
        finally:
            app.routes.pop()

    def test_unhandled_exception_handler_registered(self):
        """The generic Exception handler should be registered for unhandled errors."""
        assert Exception in app.exception_handlers, "No generic Exception handler registered"

    def test_error_response_has_details_field(self, client: TestClient):
        """Error responses can include optional details."""

        @app.get("/test/with-details")
        async def raise_with_details():
            raise NotFoundError("Not found", details={"id": 123})

        try:
            response = client.get("/test/with-details")
            data = response.json()
            assert "details" in data
            assert data["details"] == {"id": 123}
        finally:
            app.routes.pop()
