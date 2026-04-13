class AppError(Exception):
    """Base application exception."""
    pass


class ConflictError(AppError):
    """Resource already exists."""
    pass


class UnauthorizedError(AppError):
    """Authentication failed."""
    pass


class ForbiddenError(AppError):
    """Permission denied."""
    pass


class NotFoundError(AppError):
    """Resource not found."""
    pass


class ExternalServiceError(AppError):
    """Error from external service (e.g., OpenRouter)."""
    pass