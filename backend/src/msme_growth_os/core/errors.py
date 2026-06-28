class MSMEGrowthOSError(Exception):
    """Base exception for expected application errors."""


class NotImplementedBusinessLogicError(MSMEGrowthOSError):
    """Raised by placeholders that intentionally do not contain business logic yet."""

