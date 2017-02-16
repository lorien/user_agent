#!/usr/bin/env python
from __future__ import absolute_import
import re
import six
import pytest

from user_agent import (generate_user_agent, generate_navigator,
                        generate_navigator_js,
                        UserAgentRuntimeError, UserAgentInvalidRequirements)

def test_it():
    ua = generate_user_agent()
    assert len(ua) > 0


def test_platform_option():
    for x in range(100):
        ua = generate_user_agent(platform='linux')
        assert 'linux' in ua.lower()

        ua = generate_user_agent(platform='win')
        assert 'windows' in ua.lower()

        ua = generate_user_agent(platform='mac')
        assert 'mac' in ua.lower()

        with pytest.raises(UserAgentRuntimeError):
            generate_user_agent(platform=11)


def test_navigator_option():
    for x in range(100):
        ua = generate_user_agent(navigator='firefox')
        assert 'firefox' in ua.lower()

        ua = generate_user_agent(navigator='chrome')
        assert 'chrome' in ua.lower()

        ua = generate_user_agent(navigator='ie')
        assert 'msie' in ua.lower() or 'rv:11' in ua.lower()


def test_navigator_option_tuple():
    for x in range(100):
        ua = generate_user_agent(navigator=('chrome',))
        ua = generate_user_agent(navigator=('chrome', 'firefox'))
        ua = generate_user_agent(navigator=('chrome', 'firefox', 'ie'))


def test_platform_option_tuple():
    for x in range(100):
        ua = generate_user_agent(platform=('win', 'linux'))
        ua = generate_user_agent(platform=('win', 'linux', 'mac'))
        ua = generate_user_agent(platform=('win',))
        ua = generate_user_agent(platform=('linux',))
        ua = generate_user_agent(platform=('mac',))


def test_platform_navigator_option():
    for x in range(100):
        ua = generate_user_agent(platform='win', navigator='firefox')
        assert 'firefox' in ua.lower()
        assert 'windows' in ua.lower()

        ua = generate_user_agent(platform='win', navigator='chrome')
        assert 'chrome' in ua.lower()
        assert 'windows' in ua.lower()

        ua = generate_user_agent(platform='win', navigator='ie')
        assert 'msie' in ua.lower() or 'rv:11' in ua.lower()
        assert 'windows' in ua.lower()


def test_platform_linux():
    for x in range(100):
        ua = generate_user_agent(platform='linux')
        assert ua.startswith('Mozilla/5.0 (X11;')


def test_mac_chrome():
    for x in range(100):
        ua = generate_user_agent(platform='mac', navigator='chrome')
        assert re.search(r'OS X \d+_\d+(_\d+\b|\b)', ua)


def test_impossible_combination():
    for x in range(100):
        with pytest.raises(UserAgentInvalidRequirements):
            generate_user_agent(platform='linux', navigator='ie')
        with pytest.raises(UserAgentInvalidRequirements):
            generate_user_agent(platform='mac', navigator='ie')


def test_generate_navigator_js():
    for x in range(100):
        nav = generate_navigator_js()
        assert set(nav.keys()) == set(['appCodeName', 'appName', 'appVersion',
                                       'platform', 'userAgent', 'oscpu'])

        assert nav['appCodeName'] == 'Mozilla'
        assert nav['appName'] in ('Netscape', 'Microsoft Internet Explorer')


def test_data_integrity():
    for x in range(100):
        nav = generate_navigator()
        for key, val in nav.items():
            assert isinstance(val, six.string_types)


def test_platform_value():
    for x in range(100):
        nav = generate_navigator(platform='win')
        assert 'Win' in nav['platform']
        nav = generate_navigator(platform='linux')
        assert 'Linux' in nav['platform']
        #TODO: Should be mac
        #nav = generate_navigator(platform='win')
        #assert 'Win' in nav['platform']


def test_oscpu_value():
    for x in range(100):
        nav = generate_navigator(platform='win')
        assert 'Windows NT' in nav['oscpu']
        nav = generate_navigator(platform='linux')
        assert 'Linux' in nav['oscpu']
        nav = generate_navigator(platform='mac')
        assert 'Mac OS' in nav['oscpu']
