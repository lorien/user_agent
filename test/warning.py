from __future__ import absolute_import
import mock
from six import StringIO

from user_agent.warning import warn


def test_warn():
    out = StringIO()
    with mock.patch('sys.stderr', out):
        warn('abc')
    assert 'UserAgentDeprecationWarning: abc' in out.getvalue()
