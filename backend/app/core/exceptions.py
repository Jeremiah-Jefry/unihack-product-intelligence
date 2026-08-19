"""Core exception types for consistent API error handling."""

from typing import Any


class AppError(Exception):
    """Base application error."""

    def __init__(self, message: str, details: Any = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppError):
    """Resource not found."""

    pass


class ValidationError(AppError):
    """Input validation failed."""

    pass


class DependencyError(AppError):
    """External dependency unavailable."""

    pass
