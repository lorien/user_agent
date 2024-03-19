__all__ = ["UserAgentError", "InvalidOption", "InvalidOptionError"]


class UserAgentError(Exception):
    """Base class for all errors raising from the user_agent library."""


class InvalidOptionError(UserAgentError):
    """Raises when user_agent library methods are called with incorrect arguments."""


InvalidOption = InvalidOptionError  # for backward compatibility
