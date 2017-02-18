#!/usr/bin/env python
# pylint: disable=missing-docstring
from __future__ import absolute_import
import re
from subprocess import check_output
import json

import six
import pytest

from user_agent import (generate_user_agent, generate_navigator,
                        generate_navigator_js,
                        UserAgentRuntimeError, UserAgentInvalidRequirements)

def test_it():
    agent = generate_user_agent()
    assert len(agent) > 0


def test_platform_option():
    for _ in range(50):
        agent = generate_user_agent(platform='linux')
        assert 'linux' in agent.lower()

        agent = generate_user_agent(platform='win')
        assert 'windows' in agent.lower()

        agent = generate_user_agent(platform='mac')
        assert 'mac' in agent.lower()

def test_invalid_platform_option():
    with pytest.raises(UserAgentRuntimeError):
        generate_user_agent(platform=11)

    with pytest.raises(UserAgentRuntimeError):
        generate_user_agent(platform='dos')

    with pytest.raises(UserAgentRuntimeError):
        generate_user_agent(platform='win,dos')


def test_navigator_option():
    for _ in range(50):
        agent = generate_user_agent(navigator='firefox')
        assert 'firefox' in agent.lower()

        agent = generate_user_agent(navigator='chrome')
        assert 'chrome' in agent.lower()

        agent = generate_user_agent(navigator='ie')
        assert 'msie' in agent.lower() or 'rv:11' in agent.lower()


def test_invalid_navigator_option():
    with pytest.raises(UserAgentRuntimeError):
        generate_user_agent(navigator='vim')

    with pytest.raises(UserAgentRuntimeError):
        generate_user_agent(navigator='chrome,vim')


def test_navigator_option_tuple():
    for _ in range(50):
        generate_user_agent(navigator=('chrome',))
        generate_user_agent(navigator=('chrome', 'firefox'))
        generate_user_agent(navigator=('chrome', 'firefox', 'ie'))


def test_platform_option_tuple():
    for _ in range(50):
        generate_user_agent(platform=('win', 'linux'))
        generate_user_agent(platform=('win', 'linux', 'mac'))
        generate_user_agent(platform=('win',))
        generate_user_agent(platform=('linux',))
        generate_user_agent(platform=('mac',))


def test_platform_navigator_option():
    for _ in range(50):
        agent = generate_user_agent(platform='win', navigator='firefox')
        assert 'firefox' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(platform='win', navigator='chrome')
        assert 'chrome' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(platform='win', navigator='ie')
        assert 'msie' in agent.lower() or 'rv:11' in agent.lower()
        assert 'windows' in agent.lower()


def test_platform_linux():
    for _ in range(50):
        agent = generate_user_agent(platform='linux')
        assert agent.startswith('Mozilla/5.0 (X11;')


def test_mac_chrome():
    for _ in range(50):
        agent = generate_user_agent(platform='mac', navigator='chrome')
        assert re.search(r'OS X \d+_\d+(_\d+\b|\b)', agent)


def test_impossible_combination():
    for _ in range(50):
        with pytest.raises(UserAgentInvalidRequirements):
            generate_user_agent(platform='linux', navigator='ie')
        with pytest.raises(UserAgentInvalidRequirements):
            generate_user_agent(platform='mac', navigator='ie')


def test_generate_navigator_js():
    for _ in range(50):
        nav = generate_navigator_js()
        assert set(nav.keys()) == set([
            'appCodeName', 'appName', 'appVersion',
            'platform', 'userAgent', 'oscpu',
            'product', 'productSub', 'vendor', 'vendorSub',
        ])

        assert nav['appCodeName'] == 'Mozilla'
        assert nav['appName'] in ('Netscape', 'Microsoft Internet Explorer')


def test_data_integrity():
    for _ in range(50):
        nav = generate_navigator()
        for _, val in nav.items():
            assert val is None or isinstance(val, six.string_types)


def test_ua_script_simple():
    for _ in range(5):
        out = (check_output('ua', shell=True)
               .decode('utf-8'))
        assert re.match('^Mozilla', out)
        assert len(out.strip().splitlines()) == 1


def test_ua_script_options():
    for _ in range(5):
        out = (check_output('ua -p linux -n chrome', shell=True)
               .decode('utf-8'))
        assert re.match('^Mozilla.*Linux.*Chrome', out)


def test_ua_script_extended():
    for _ in range(5):
        out = (check_output('ua -p linux -n chrome -e', shell=True)
               .decode('utf-8'))
        data = json.loads(out)
        assert 'Linux' in data['platform']
        assert 'Chrome' in data['userAgent']


def test_feature_platform():
    for _ in range(50):
        nav = generate_navigator(platform='win')
        assert 'Win' in nav['platform']
        nav = generate_navigator(platform='linux')
        assert 'Linux' in nav['platform']
        #TODO: Should be mac
        #nav = generate_navigator(platform='win')
        #assert 'Win' in nav['platform']


def test_feature_oscpu():
    for _ in range(10):
        nav = generate_navigator(platform='win')
        assert 'Windows NT' in nav['oscpu']
        nav = generate_navigator(platform='linux')
        assert 'Linux' in nav['oscpu']
        nav = generate_navigator(platform='mac')
        assert 'Mac OS' in nav['oscpu']


def test_feature_chrome_appversion():
    for _ in range(50):
        nav = generate_navigator_js(navigator='chrome')
        assert ('Mozilla/' + nav['appVersion']) == nav['userAgent']


def test_feature_product():
    for _ in range(50):
        nav = generate_navigator_js(navigator='chrome')
        assert nav['product'] == 'Gecko'


def test_feature_vendor_sub():
    for _ in range(50):
        nav = generate_navigator_js(navigator='chrome')
        assert nav['vendor'] == 'Google Inc.'
        nav = generate_navigator_js(navigator='firefox')
        assert nav['vendor'] == ''
        nav = generate_navigator_js(navigator='ie')
        assert nav['vendor'] == ''


def test_feature_vendor_sub():
    for _ in range(50):
        nav = generate_navigator_js(navigator='chrome')
        assert nav['vendorSub'] == ''
