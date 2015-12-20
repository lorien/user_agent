# -*- coding: utf-8 -*-
"""
This module is for generating random, valid web navigator's configs & User-Agent HTTP headers.
** generate_user_agent: generates User-Agent HTTP header
** generate_navigator:  generates web navigator's config

TODO:
* add Edge, Safari and Opera support
* add random config i.e. win platform more common than linux

Specs:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Gecko_user_agent_string_reference
* http://msdn.microsoft.com/en-us/library/ms537503(VS.85).aspx
* https://developer.chrome.com/multidevice/user-agent

Release history:
* https://en.wikipedia.org/wiki/Firefox_release_history
* https://en.wikipedia.org/wiki/Google_Chrome_release_history

Lists of user agents:
* http://www.useragentstring.com/
* http://www.user-agents.org/ 
* http://www.webapps-online.com/online-tools/user-agent-strings

"""

from random import choice, randint
import six

__all__ = ['generate_user_agent', 'generate_navigator',
           'UserAgentRuntimeError', 'UserAgentInvalidRequirements']

PLATFORM = {
    'win': (
        'Windows NT 5.1', # Windows XP
        'Windows NT 6.1', # Windows 7
        'Windows NT 6.2', # Windows 8
        'Windows NT 6.3', # Windows 8.1
        'Windows NT 10.0', # Windows 10
    ),
    'mac': (
        'Macintosh; Intel Mac OS X 10.8',
        'Macintosh; Intel Mac OS X 10.9',
        'Macintosh; Intel Mac OS X 10.10',
        'Macintosh; Intel Mac OS X 10.11',
    ),
    'linux': (
        'X11; Linux',
        'X11; Ubuntu; Linux',
    ),
}

SUBPLATFORM = {
    'win': (
        ('', 'Win32'), # 32bit
        ('Win64; x64', 'Win32'), # 64bit
        ('WOW64', 'Win32'), # 32bit process / 64bit system
    ),
    'linux': (
        ('i686', 'Linux i686'), # 32bit
        ('x86_64', 'Linux x86_64'), # 64bit
        ('i686 on x86_64', 'Linux i686 on x86_64'), # 32bit process / 64bit system
    ),
    'mac': (
        ('MacIntel',), # 32bit, 64bit
    ),
}

PLATFORM_NAVIGATORS = {
    'win': ('chrome', 'firefox', 'ie'),
    'mac': ('firefox', 'chrome'),
    'linux': ('chrome', 'firefox'),
}

NAVIGATOR_PLATFORMS = {
    'chrome': ('win', 'linux', 'mac'),
    'firefox': ('win', 'linux', 'mac'),
    'ie': ('win',),
}

NAVIGATOR = ('firefox', 'chrome', 'ie')
APPVERSION = '5.0'
USERAGENT_TEMPLATE = {
    'ie': (
        'Mozilla/5.0 (compatible; MSIE %(version)s; %(platform)s'
    ),

}
FIREFOX_VERSION = (
    '27.0', '28.0', '29.0', '31.0', '33.0', '36.0', '37.0', '38.0',
    '39.0', '40.0', '41.0', '42.0', '43.0',
)
GECKOTRAIL_DESKTOP = '20100101'
CHROME_BUILD = (
    (32, 1700, 1749),
    (33, 1750, 1846),
    (34, 1847, 1915),
    (35, 1916, 1984),
    (36, 1985, 2061),
    (37, 2062, 2124),
    (38, 2125, 2170),
    (39, 2171, 2213),
    (40, 2214, 2271),
    (41, 2272, 2310),
    (42, 2311, 2356),
    (43, 2357, 2402),
    (44, 2403, 2453),
    (45, 2454, 2489),
)
IE_VERSION = (
    'MSIE 11.0',
    'MSIE 10.0',
    'MSIE 9.0',
    'MSIE 8.0',
)


class UserAgentRuntimeError(Exception):
    pass


class UserAgentInvalidRequirements(UserAgentRuntimeError):
    pass


def build_ua(navigator_name, navigator_version, platform):
    assert navigator_name in ('firefox', 'chrome', 'ie')
    if navigator_name == 'firefox':
        return ('Mozilla/5.0 (%s; rv:%s) Gecko/%s Firefox/%s'
                % (platform, navigator_version,
                   GECKOTRAIL_DESKTOP, navigator_version))
    elif navigator_name == 'chrome':
        return ('Mozilla/5.0 (%s) AppleWebKit/537.36 (KHTML, like Gecko)'
                ' Chrome/%s Safari/537.36'
                % (platform, navigator_version))
    elif navigator_name == 'ie':
        if navigator_version == 'MSIE 11.0':
            return ('Mozilla/5.0 (%s; Trident/7.0; rv:11.0) like Gecko'
                    % platform)
        else:
            return ('Mozilla/5.0 (compatible; %s; %s)'
                    % (navigator_version, platform))  

def build_firefox_version():
    return choice(FIREFOX_VERSION)


def build_chrome_version():
    build = choice(CHROME_BUILD)
    return '%d.0.%d.%d' % (
        build[0],
        randint(build[1], build[2]),
        randint(0, 99),
    )


def build_ie_version():
    return choice(IE_VERSION)


MACOSX_CHROME_BUILD_RANGE = {
    '10.8': (0, 8),
    '10.9': (0, 5),
    '10.10': (0, 5),
    '10.11': (0, 1),
}


def fix_chrome_mac_platform(platform):
    """
    :param platform: - string like "Macintosh; Intel Mac OS X 10.8"
    """
    ver = platform.split('OS X ')[1]
    build_range = list(MACOSX_CHROME_BUILD_RANGE[ver])
    #build_range.append(None)
    build = choice(build_range)
    #if build is None:
    #    mac_ver = ver.replace('.', '_')
    #else:
    mac_ver = ver.replace('.', '_') + '_' + str(build)
    return 'Macintosh; Intel Mac OS X %s' % mac_ver


def generate_navigator(platform=None, navigator=None):
    """
    Generates web navigator's config

    :param platform: limit list of platforms for generation
    :type platform: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :return: User-Agent config
    :rtype: dict with keys (appversion, name, os, oscpu,
                            platform, user_agent, version)
    :raises UserAgentInvalidRequirements: if could not generate user-agent for
        any combination of allowed platforms and navigators
    :raise UserAgentRuntimeError: if any of passed options is invalid
    """

    # Process platform option
    if isinstance(platform, six.string_types):
        platform_choices = [platform]
    elif isinstance(platform, (list, tuple)):
        platform_choices = list(platform)
    elif platform is None:
        platform_choices = list(PLATFORM.keys())
    else:
        raise UserAgentRuntimeError('Option platform has invalid'
                                    ' value: %s' % platform)

    # Process navigator option
    if isinstance(navigator, six.string_types):
        navigator_choices = [navigator]
    elif isinstance(navigator, (list, tuple)):
        navigator_choices = list(navigator)
    elif navigator is None:
        navigator_choices = list(NAVIGATOR)
    else:
        raise UserAgentRuntimeError('Option navigator has invalid'
                                    ' value: %s' % navigator)

    # If we have only one navigator option to choose from
    # Then use it and select platform from platforms
    # available for choosen navigator
    if len(navigator_choices) == 1:
        navigator_name = navigator_choices[0]
        avail_platform_choices = [x for x in platform_choices
                                  if x in NAVIGATOR_PLATFORMS[navigator_name]]
        # This list could be empty because of invalid
        # parameters passed to the `generate_navigator` function
        if avail_platform_choices:
            platform_name = choice(avail_platform_choices)
        else:
            platform_list = '[%s]' % ', '.join(avail_platform_choices)
            navigator_list = '[%s]' % ', '.join(navigator_choices)
            raise UserAgentInvalidRequirements(
                'Could not generate navigator for any combination of'
                ' %s platforms and %s navigators'
                % (platform_list, navigator_list))
    else:
        platform_name = choice(platform_choices)
        avail_navigator_choices = [x for x in navigator_choices
                                   if x in PLATFORM_NAVIGATORS[platform_name]]
        # This list could be empty because of invalid
        # parameters passed to the `generate_navigator` function
        if avail_navigator_choices:
            navigator_name = choice(avail_navigator_choices)
        else:
            platform_list = '[%s]' % ', '.join(avail_platform_choices)
            navigator_list = '[%s]' % ', '.join(navigator_choices)
            raise UserAgentInvalidRequirements(
                'Could not generate navigator for any combination of'
                ' %s platforms and %s navigators'
                % (platform_list, navigator_list))

    assert platform_name in PLATFORM
    assert navigator_name in NAVIGATOR

    if platform_name == 'win':
        subplatform, navigator_platform = choice(SUBPLATFORM['win'])
        win_platform = choice(PLATFORM['win'])
        if subplatform:
            platform = win_platform + '; ' + subplatform
        else:
            platform = win_platform
        oscpu = platform
    elif platform_name == 'linux':
        subplatform, navigator_platform = choice(SUBPLATFORM['linux'])
        platform = choice(PLATFORM['linux']) + ' ' + subplatform
        oscpu = navigator_platform
    elif platform_name == 'mac':
        navigator_platform = SUBPLATFORM['mac']
        platform = choice(PLATFORM['mac'])
        if navigator_name == 'chrome':
            platform = fix_chrome_mac_platform(platform)
        oscpu = platform[11:]

    if navigator_name == 'firefox':
        navigator_version = build_firefox_version()
    elif navigator_name == 'chrome':
        navigator_version = build_chrome_version()
    elif navigator_name == 'ie':
        navigator_version = build_ie_version()

    user_agent = build_ua(navigator_name, navigator_version, platform)

    return {
        'name': navigator_name,
        'version': navigator_version,
        'os': platform_name,
        'platform': navigator_platform,
        'oscpu': oscpu,
        'user_agent': user_agent,
        'appversion': APPVERSION,
    }


def generate_user_agent(platform=None, navigator=None):
    """
    Generates HTTP User-Agent header

    :param platform: limit list of platforms for generation
    :type platform: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :return: User-Agent string
    :rtype: string
    :raises UserAgentInvalidRequirements: if could not generate user-agent for
        any combination of allowed platforms and navigators
    :raise UserAgentRuntimeError: if any of passed options is invalid
    """
    return generate_navigator(platform=platform, navigator=navigator)['user_agent']
