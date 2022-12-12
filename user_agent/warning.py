import warnings


class UserAgentDeprecationWarning(UserWarning):
    """Warns about deprecated feature of user_agent library."""


def warn(msg: str, stacklevel: int = 2) -> None:
    warnings.warn(msg, category=UserAgentDeprecationWarning, stacklevel=stacklevel)
