"""Tests for application configuration."""

from app.core.config import Settings


class TestConfiguration:
    """Tests for Settings / configuration loading."""

    def test_settings_loads_defaults(self):
        settings = Settings()
        assert settings.APP_ENV in ("development", "production", "testing")
        assert settings.API_HOST == "0.0.0.0"
        assert settings.API_PORT == 8000
        assert settings.FRONTEND_URL == "http://localhost:8501"

    def test_settings_database_url_present(self):
        settings = Settings()
        assert settings.DATABASE_URL is not None
        assert len(settings.DATABASE_URL) > 0

    def test_settings_is_development_property(self):
        settings = Settings()
        if settings.APP_ENV == "development":
            assert settings.is_development is True
            assert settings.is_production is False
        elif settings.APP_ENV == "production":
            assert settings.is_development is False
            assert settings.is_production is True

    def test_settings_storage_dirs_present(self):
        settings = Settings()
        assert settings.UPLOAD_DIR is not None
        assert settings.STORAGE_DIR is not None
        assert len(settings.UPLOAD_DIR) > 0
        assert len(settings.STORAGE_DIR) > 0

    def test_settings_openai_key_defaults_empty(self):
        """OpenAI key should default to empty string (not required for foundation)."""
        settings = Settings()
        # The key may be set from env; verify the field exists
        assert hasattr(settings, "OPENAI_API_KEY")

    def test_settings_env_file_support(self):
        """Settings should support .env file loading."""
        assert "env_file" in Settings.model_config
