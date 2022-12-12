__all__ = ["UserAgentError", "InvalidOption"]


class UserAgentError(Exception):
    """Base class for all errors raising from the user_agent library."""


class InvalidOption(UserAgentError):
    """Raises when user_agent library methods are called with incorrect arguments."""
