# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
This module is for generating random, valid web navigator's
    configs & User-Agent HTTP headers.

Functions:
* generate_user_agent: generates User-Agent HTTP header
* generate_navigator:  generates web navigator's config

FIXME:
* add Edge, Safari and Opera support
* add random config i.e. win platform more common than linux

Specs:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent/Firefox
* http://msdn.microsoft.com/en-us/library/ms537503(VS.85).aspx
* https://developer.chrome.com/multidevice/user-agent
* http://www.javascriptkit.com/javatutors/navigator.shtml

Release history:
* https://en.wikipedia.org/wiki/Firefox_release_history
* https://en.wikipedia.org/wiki/Google_Chrome_release_history
* https://en.wikipedia.org/wiki/Internet_Explorer_version_history

Lists of user agents:
* http://www.useragentstring.com/
* http://www.user-agents.org/
* http://www.webapps-online.com/online-tools/user-agent-strings

"""
# pylint: enable=line-too-long

from random import choice, randint
import six

__all__ = ['generate_user_agent', 'generate_navigator',
           'generate_navigator_js',
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
        'Macintosh; Intel Mac OS X 10.12',
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
        ('i686 on x86_64', 'Linux i686 on x86_64'), # 32bit process on 64bit os
    ),
    'mac': (
        ('', 'MacIntel'),
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
    'ie': 'Mozilla/5.0 (compatible; MSIE %(version)s; %(platform)s',
}
FIREFOX_VERSION = (
    '45.0', # 2016-03-08
    '46.0', # 2016-04-26
    '47.0', # 2016-06-07
    '48.0', # 2016-08-02
    '49.0', # 2016-09-20
    '50.0', # 2016-11-15
    '51.0', # 2017-01-24
)
GECKOTRAIL_DESKTOP = '20100101'
CHROME_BUILD = (
    (49, 2623, 2660), # 2016-03-02
    (50, 2661, 2703), # 2016-04-13
    (51, 2704, 2742), # 2016-05-25
    (52, 2743, 2784), # 2016-07-20
    (53, 2785, 2839), # 2016-08-31
    (54, 2840, 2882), # 2016-10-12
    (55, 2883, 2923), # 2016-12-01
    (56, 2924, 2986), # 2016-12-01
)
IE_VERSION = (
    (8, 'MSIE 8.0'), # 2009
    (9, 'MSIE 9.0'), # 2011
    (10, 'MSIE 10.0'), # 2012
    (11, 'MSIE 11.0'), # 2013
)
USER_AGENT_TEMPLATE = {
    'firefox': (
        'Mozilla/5.0'
        ' ({platform}; rv:{app_version}) Gecko/20100101'
        ' Firefox/{app_version}'
    ),
    'chrome': (
        'Mozilla/5.0'
        ' ({platform}) AppleWebKit/537.36'
        ' (KHTML, like Gecko)'
        ' Chrome/{app_version} Safari/537.36'
    ),
    'ie_old': (
        'Mozilla/5.0'
        ' (compatible; {app_version}; {platform})'
    ),
    'ie_new': (
        'Mozilla/5.0'
        ' ({platform}; Trident/7.0; rv:11.0) like Gecko'
    ),
}


class UserAgentRuntimeError(Exception):
    pass


class UserAgentInvalidRequirements(UserAgentRuntimeError):
    pass


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
    """
    Return random IE version as tuple
    (numeric_version, us-string component)

    Example: (8, 'MSIE 8.0')
    """

    return choice(IE_VERSION)


MACOSX_CHROME_BUILD_RANGE = {
    # https://en.wikipedia.org/wiki/MacOS#Release_history
    '10.8': (0, 8),
    '10.9': (0, 5),
    '10.10': (0, 5),
    '10.11': (0, 6),
    '10.12': (0, 2)
}


def fix_chrome_mac_platform(platform):
    """
    Chrome on Mac OS adds minor version number and uses underscores instead
    of dots. E.g. platform for Firefox will be: 'Intel Mac OS X 10.11'
    but for Chrome it will be 'Intel Mac OS X 10_11_6'.

    :param platform: - string like "Macintosh; Intel Mac OS X 10.8"
    :return: platform with version number including minor number and formatted
    with underscores, e.g. "Macintosh; Intel Mac OS X 10_8_2"
    """
    ver = platform.split('OS X ')[1]
    build_range = range(*MACOSX_CHROME_BUILD_RANGE[ver])
    build = choice(build_range)
    mac_ver = ver.replace('.', '_') + '_' + str(build)
    return 'Macintosh; Intel Mac OS X %s' % mac_ver


def build_platform_components(platform_name, navigator_name):
    """
    For given platform_name build random platform and oscpu
    components

    Returns tuple (platform, oscpu)
    """

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
        subplatform, navigator_platform = choice(SUBPLATFORM['mac'])
        platform = choice(PLATFORM['mac'])
        oscpu = 'Intel Mac OS X %s' % platform.split(' ')[-1]
        if navigator_name == 'chrome':
            platform = fix_chrome_mac_platform(platform)
    return platform, oscpu


def build_app_components(navigator_name):
    """
    For given navigator_name build random app version and app name
    components

    Returns tuple (platform, oscpu)
    """

    if navigator_name == 'firefox':
        app_version = build_firefox_version()
        app_name = 'Netscape'
    elif navigator_name == 'chrome':
        app_version = build_chrome_version()
        app_name = 'Netscape'
    elif navigator_name == 'ie':
        num_ver, app_version = build_ie_version()
        if num_ver >= 11:
            app_name = 'Netscape'
        else:
            app_name = 'Microsoft Internet Explorer'
    return app_version, app_name


def pickup_platform_navigator_ids(platform, navigator):
    """
    Select one random pair (platform_id, navigator_id) from all
    possible combinations matching the given platform and
    navigator filters.

    :param platform: allowed platform(s)
    :type platform: string or list/tuple or None
    :param navigator: allowed browser engine(s)
    :type navigator: string or list/tuple or None
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
    for item in platform_choices:
        if item not in PLATFORM_NAVIGATORS:
            raise UserAgentRuntimeError('Invalid platform option: %s' % item)

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
    for item in navigator_choices:
        if item not in NAVIGATOR_PLATFORMS:
            raise UserAgentRuntimeError('Invalid navigator option: %s' % item)

    # If we have only one navigator option to choose from
    # Then use it and select platform from platforms
    # available for choosen navigator
    if len(navigator_choices) == 1:
        navigator_id = navigator_choices[0]
        avail_platform_choices = [x for x in platform_choices
                                  if x in NAVIGATOR_PLATFORMS[navigator_id]]
        # This list could be empty because of invalid
        # parameters passed to the `generate_navigator` function
        if avail_platform_choices:
            platform_id = choice(avail_platform_choices)
        else:
            platform_list = '[%s]' % ', '.join(avail_platform_choices)
            navigator_list = '[%s]' % ', '.join(navigator_choices)
            raise UserAgentInvalidRequirements(
                'Could not generate navigator for any combination of'
                ' %s platforms and %s navigators'
                % (platform_list, navigator_list))
    else:
        platform_id = choice(platform_choices)
        avail_navigator_choices = [x for x in navigator_choices
                                   if x in PLATFORM_NAVIGATORS[platform_id]]
        # This list could be empty because of invalid
        # parameters passed to the `generate_navigator` function
        if avail_navigator_choices:
            navigator_id = choice(avail_navigator_choices)
        else:
            platform_list = '[%s]' % ', '.join(avail_platform_choices)
            navigator_list = '[%s]' % ', '.join(navigator_choices)
            raise UserAgentInvalidRequirements(
                'Could not generate navigator for any combination of'
                ' %s platforms and %s navigators'
                % (platform_list, navigator_list))

    assert platform_id in PLATFORM
    assert navigator_id in NAVIGATOR

    return platform_id, navigator_id


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

    platform_id, navigator_id = pickup_platform_navigator_ids(platform,
                                                              navigator)
    os_platform, oscpu = build_platform_components(platform_id,
                                                   navigator_id)
    app_version, app_name = build_app_components(navigator_id)
    if navigator_id == 'ie':
        tpl_name = 'ie_new' if app_version == 'MSIE 11.0' else 'ie_old'
    else:
        tpl_name = navigator_id
    ua_template = USER_AGENT_TEMPLATE[tpl_name]
    user_agent = ua_template.format(
        platform=os_platform,
        app_version=app_version,
    )

    return {
        # ids
        'os': platform_id,
        'name': navigator_id,
        # platform components
        'platform': os_platform,
        'oscpu': oscpu,
        # app components
        'appversion': APPVERSION,
        'version': app_version,
        'app_name': app_name,
        'app_code_name': 'Mozilla',
        # compiled user agent
        'user_agent': user_agent,
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
    return generate_navigator(platform=platform,
                              navigator=navigator)['user_agent']


def generate_navigator_js(platform=None, navigator=None):
    """
    Generates web navigator's config with keys corresponding
    to keys of `windows.navigator` JavaScript object.

    :param platform: limit list of platforms for generation
    :type platform: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :return: User-Agent config
    :rtype: dict with keys (TODO)
    :raises UserAgentInvalidRequirements: if could not generate user-agent for
        any combination of allowed platforms and navigators
    :raise UserAgentRuntimeError: if any of passed options is invalid
    """

    config = generate_navigator(platform=platform, navigator=navigator)
    return {
        'appCodeName': config['app_code_name'],
        'appName': config['app_name'],
        'appVersion': config['version'],
        'platform': config['platform'],
        'userAgent': config['user_agent'],
        'oscpu': config['oscpu'],
    }
