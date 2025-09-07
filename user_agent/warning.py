import warnings


class UserAgentDeprecationWarning(UserWarning):
    """Warns about deprecated feature of user_agent library."""


def warn(msg, stacklevel=2):
    # type: (str, int) -> None
    warnings.warn(msg, category=UserAgentDeprecationWarning, stacklevel=stacklevel)
