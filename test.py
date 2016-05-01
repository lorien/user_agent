#!/usr/bin/env python
from unittest import TestCase
import unittest
import re
import six

from user_agent import (generate_user_agent, generate_navigator,
                        generate_navigator_js,
                        UserAgentRuntimeError, UserAgentInvalidRequirements)

class UserAgentTestCase(TestCase):
    def test_it(self):
        ua = generate_user_agent()
        self.assertTrue(len(ua) > 0)

    def test_platform_option(self):
        for x in range(100):
            ua = generate_user_agent(platform='linux')
            self.assertTrue('linux' in ua.lower())

            ua = generate_user_agent(platform='win')
            self.assertTrue('windows' in ua.lower())

            ua = generate_user_agent(platform='mac')
            self.assertTrue('mac' in ua.lower())

            self.assertRaises(UserAgentRuntimeError,
                              generate_user_agent,
                              platform=11)

    def test_navigator_option(self):
        for x in range(100):
            ua = generate_user_agent(navigator='firefox')
            self.assertTrue('firefox' in ua.lower())

            ua = generate_user_agent(navigator='chrome')
            self.assertTrue('chrome' in ua.lower())

            ua = generate_user_agent(navigator='ie')
            self.assertTrue('msie' in ua.lower() or 'rv:11' in ua.lower())

    def test_navigator_option_tuple(self):
        for x in range(100):
            ua = generate_user_agent(navigator=('chrome',))
            ua = generate_user_agent(navigator=('chrome', 'firefox'))
            ua = generate_user_agent(navigator=('chrome', 'firefox', 'ie'))

    def test_platform_option_tuple(self):
        for x in range(100):
            ua = generate_user_agent(platform=('win', 'linux'))
            ua = generate_user_agent(platform=('win', 'linux', 'mac'))
            ua = generate_user_agent(platform=('win',))
            ua = generate_user_agent(platform=('linux',))
            ua = generate_user_agent(platform=('mac',))

    def test_platform_navigator_option(self):
        for x in range(100):
            ua = generate_user_agent(platform='win', navigator='firefox')
            self.assertTrue('firefox' in ua.lower())
            self.assertTrue('windows' in ua.lower())

            ua = generate_user_agent(platform='win', navigator='chrome')
            self.assertTrue('chrome' in ua.lower())
            self.assertTrue('windows' in ua.lower())

            ua = generate_user_agent(platform='win', navigator='ie')
            self.assertTrue('msie' in ua.lower() or 'rv:11' in ua.lower())
            self.assertTrue('windows' in ua.lower())

    def test_platform_linux(self):
        for x in range(100):
            ua = generate_user_agent(platform='linux')
            self.assertTrue(ua.startswith('Mozilla/5.0 (X11;'))

    def test_mac_chrome(self):
        for x in range(100):
            ua = generate_user_agent(platform='mac', navigator='chrome')
            self.assertTrue(re.search(r'OS X \d+_\d+(_\d+\b|\b)', ua))

    def test_impossible_combination(self):
        for x in range(100):
            self.assertRaises(UserAgentInvalidRequirements,
                              generate_user_agent,
                              platform='linux', navigator='ie')
            self.assertRaises(UserAgentInvalidRequirements,
                              generate_user_agent,
                              platform='mac', navigator='ie')

    def test_generate_navigator_js(self):
        for x in range(100):
            nav = generate_navigator_js()
            self.assertEqual(set(['appCodeName', 'appName', 'appVersion',
                                  'platform', 'userAgent', 'oscpu'
                                  ]), set(nav.keys()))

            self.assertEqual(nav['appCodeName'], 'Mozilla')
            self.assertTrue(nav['appName'] in (
                'Netscape', 'Microsoft Internet Explorer'))

    def test_data_integrity(self):
        for x in range(100):
            nav = generate_navigator()
            for key, val in nav.items():
                self.assertTrue(isinstance(val, six.string_types))

    def test_platform_value(self):
        for x in range(100):
            nav = generate_navigator(platform='win')
            self.assertTrue('Win' in nav['platform'])
            nav = generate_navigator(platform='linux')
            self.assertTrue('Linux' in nav['platform'])
            #TODO: Should be mac
            #nav = generate_navigator(platform='win')
            #self.assertTrue('Win' in nav['platform'])

    def test_oscpu_value(self):
        for x in range(100):
            nav = generate_navigator(platform='win')
            self.assertTrue('Windows NT' in nav['oscpu'])
            nav = generate_navigator(platform='linux')
            self.assertTrue('Linux' in nav['oscpu'])
            nav = generate_navigator(platform='mac')
            self.assertTrue('Mac OS' in nav['oscpu'])





if __name__ == '__main__':
    unittest.main()
