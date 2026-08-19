"""Tests for database integration."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import Base, get_db
from app.models.health_check import HealthCheck


class TestDatabaseConnection:
    """Tests for database connectivity and session management."""

    def test_database_connection_succeeds(self, db_session: Session):
        result = db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1

    def test_health_check_table_exists(self, db_session: Session):
        """The health_check table should exist after migration/create_all."""
        result = db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='health_check'")
        )
        table = result.scalar()
        assert table == "health_check"

    def test_health_check_insert_and_read(self, db_session: Session):
        """Can insert and read from the health_check table."""
        record = HealthCheck(status="ok")
        db_session.add(record)
        db_session.flush()

        result = db_session.execute(
            text("SELECT status FROM health_check WHERE id = :id"),
            {"id": record.id},
        )
        row = result.scalar()
        assert row == "ok"

    def test_health_check_default_status(self, db_session: Session):
        """HealthCheck record should have default status 'ok'."""
        record = HealthCheck()
        db_session.add(record)
        db_session.flush()
        assert record.status == "ok"

    def test_health_check_created_at(self, db_session: Session):
        """HealthCheck record should have a created_at timestamp."""
        record = HealthCheck()
        db_session.add(record)
        db_session.flush()
        assert record.created_at is not None

    def test_database_session_yields_and_closes(self, db_session: Session):
        """The get_db dependency should yield a session and close it."""
        session = next(get_db())
        try:
            assert session is not None
            result = session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        finally:
            session.close()

    def test_multiple_sessions_can_coexist(self, db_session: Session):
        """Multiple sessions should work against the same database."""
        record1 = HealthCheck(status="ok")
        record2 = HealthCheck(status="ok")
        db_session.add(record1)
        db_session.add(record2)
        db_session.flush()

        result = db_session.execute(text("SELECT COUNT(*) FROM health_check"))
        count = result.scalar()
        assert count >= 2

    def test_base_metadata_has_models(self):
        """The Base metadata should have the HealthCheck model registered."""
        table_names = list(Base.metadata.tables.keys())
        assert "health_check" in table_names
