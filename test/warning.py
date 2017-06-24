#from __future__ import absolute_import
#import mock
#from six import StringIO
#
#from user_agent.warning import warn

# TODO: Fix, it does not work
# https://travis-ci.org/lorien/user_agent/jobs/246368181
#def test_warn():
#    out = StringIO()
#    with mock.patch('sys.stderr', out):
#        warn('abc')
#    assert 'UserAgentDeprecationWarning: abc' in out.getvalue()
