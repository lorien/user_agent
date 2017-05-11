#!/usr/bin/env python
# pylint: disable=missing-docstring
from __future__ import absolute_import
import re
from subprocess import check_output
import json
from datetime import datetime
from copy import deepcopy

import six
import pytest

from user_agent import (generate_user_agent, generate_navigator,
                        generate_navigator_js, InvalidOption)


def test_it():
    agent = generate_user_agent()
    assert len(agent) > 0 # pylint: disable=len-as-condition


def test_platform_option():
    for _ in range(50):
        agent = generate_user_agent(os='linux')
        assert 'linux' in agent.lower()

        agent = generate_user_agent(os='win')
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='mac')
        assert 'mac' in agent.lower()


def test_invalid_platform_option():
    with pytest.raises(InvalidOption):
        generate_user_agent(os=11)

    with pytest.raises(InvalidOption):
        generate_user_agent(os='dos')

    with pytest.raises(InvalidOption):
        generate_user_agent(os='win,dos')


def test_navigator_option():
    for _ in range(50):
        agent = generate_user_agent(navigator='firefox')
        assert 'firefox' in agent.lower()

        agent = generate_user_agent(navigator='chrome')
        assert 'chrome' in agent.lower()

        agent = generate_user_agent(navigator='ie')
        assert 'msie' in agent.lower() or 'rv:11' in agent.lower()


def test_invalid_navigator_option():
    with pytest.raises(InvalidOption):
        generate_user_agent(navigator='vim')

    with pytest.raises(InvalidOption):
        generate_user_agent(navigator='chrome,vim')


def test_navigator_option_tuple():
    for _ in range(50):
        generate_user_agent(navigator=('chrome',))
        generate_user_agent(navigator=('chrome', 'firefox'))
        generate_user_agent(navigator=('chrome', 'firefox', 'ie'))


def test_platform_option_tuple():
    for _ in range(50):
        generate_user_agent(os=('win', 'linux'))
        generate_user_agent(os=('win', 'linux', 'mac'))
        generate_user_agent(os=('win',))
        generate_user_agent(os=('linux',))
        generate_user_agent(os=('mac',))


def test_platform_navigator_option():
    for _ in range(50):
        agent = generate_user_agent(os='win', navigator='firefox')
        assert 'firefox' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='win', navigator='chrome')
        assert 'chrome' in agent.lower()
        assert 'windows' in agent.lower()

        agent = generate_user_agent(os='win', navigator='ie')
        assert 'msie' in agent.lower() or 'rv:11' in agent.lower()
        assert 'windows' in agent.lower()


def test_platform_linux():
    for _ in range(50):
        agent = generate_user_agent(os='linux')
        assert agent.startswith('Mozilla/5.0 (X11;')


def test_mac_chrome():
    for _ in range(50):
        agent = generate_user_agent(os='mac', navigator='chrome')
        assert re.search(r'OS X \d+_\d+(_\d+\b|\b)', agent)


def test_impossible_combination():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(os='linux', navigator='ie')
        with pytest.raises(InvalidOption):
            generate_user_agent(os='mac', navigator='ie')


def test_generate_navigator_js():
    for _ in range(50):
        nav = generate_navigator_js()
        assert set(nav.keys()) == set([
            'appCodeName', 'appName', 'appVersion',
            'platform', 'userAgent', 'oscpu',
            'product', 'productSub', 'vendor', 'vendorSub',
            'buildID',
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
        out = (check_output('ua -o linux -n chrome', shell=True)
               .decode('utf-8'))
        assert re.match('^Mozilla.*Linux.*Chrome', out)


def test_ua_script_extended():
    for _ in range(5):
        out = (check_output('ua -o linux -n chrome -e', shell=True)
               .decode('utf-8'))
        data = json.loads(out)
        assert 'Linux' in data['platform']
        assert 'Chrome' in data['userAgent']


def test_feature_platform():
    for _ in range(50):
        nav = generate_navigator(os='win')
        assert 'Win' in nav['platform']
        nav = generate_navigator(os='linux')
        assert 'Linux' in nav['platform']
        #TODO: Should be mac
        #nav = generate_navigator(os='win')
        #assert 'Win' in nav['platform']


def test_feature_oscpu():
    for _ in range(10):
        nav = generate_navigator(os='win')
        assert 'Windows NT' in nav['oscpu']
        nav = generate_navigator(os='linux')
        assert 'Linux' in nav['oscpu']
        nav = generate_navigator(os='mac')
        assert 'Mac OS' in nav['oscpu']


def test_feature_chrome_appversion():
    for _ in range(50):
        nav = generate_navigator_js(navigator='chrome')
        assert ('Mozilla/' + nav['appVersion']) == nav['userAgent']


def test_feature_product():
    for _ in range(50):
        nav = generate_navigator_js(navigator='chrome')
        assert nav['product'] == 'Gecko'


def test_feature_vendor():
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


def test_build_id_nofirefox():
    for _ in range(50):
        nav = generate_navigator(navigator='chrome')
        assert nav['build_id'] is None
        nav = generate_navigator(navigator='ie')
        assert nav['build_id'] is None


def test_build_id_firefox():
    from user_agent import base

    orig_ff_ver = deepcopy(base.FIREFOX_VERSION)
    base.FIREFOX_VERSION = [
        ('49.0', datetime(2016, 9, 20)),
        ('50.0', datetime(2016, 11, 15)),
    ]
    try:
        for _ in range(50):
            nav = generate_navigator(navigator='firefox')
            assert len(nav['build_id']) == 14
            if '50.0' in nav['user_agent']:
                assert nav['build_id'].startswith('20161115')
            else:
                time_ = datetime.strptime(nav['build_id'], '%Y%m%d%H%M%S')
                assert datetime(2016, 9, 20, 0) <= time_
                assert time_ < datetime(2016, 11, 15)
    finally:
        base.FIREFOX_VERSION = orig_ff_ver


def test_android_firefox():
    for _ in range(50):
        nav = generate_navigator_js(os='android', navigator='firefox')
        assert 'armv' in nav['platform']
        assert 'Linux armv' in nav['oscpu']
        assert 'Android' in nav['userAgent'].split('(')[1].split(')')[0]
        assert 'Android' in nav['appVersion']


def test_device_type_option():
    for _ in range(50):
        agent = generate_user_agent(device_type='desktop')
        agent = generate_user_agent(device_type='smartphone')
        assert 'Android' in agent
        assert 'Firefox' in agent or 'Chrome' in agent


def test_device_type_option_invalid():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(device_type='fridge')


def test_invalid_combination_device_type_os():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(device_type='smartphone', os='win')


def test_invalid_combination_device_type_navigator():
    for _ in range(50):
        with pytest.raises(InvalidOption):
            generate_user_agent(device_type='smartphone', navigator='ie')


def test_no_os_options_default_device_type():
    for _ in range(50):
        agent = generate_user_agent()
        # by default if no os option has given
        # then device_type is "desktop"
        assert 'Android' not in agent


def test_device_type_all():
    for _ in range(50):
        generate_user_agent(device_type='all')
        generate_user_agent(device_type='all', navigator='ie')


def test_device_type_smartphone_chrome():
    for _ in range(50):
        agent = generate_user_agent(device_type='smartphone',
                                    navigator='chrome')
        assert 'Mobile' in agent
        agent = generate_user_agent(device_type='tablet', navigator='chrome')
        assert 'Mobile' not in agent
