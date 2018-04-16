# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
This module is for generating random, valid web navigator's
    configs & User-Agent HTTP headers.

Functions:
* generate_user_agent: generates User-Agent HTTP header
* generate_navigator:  generates web navigator's config
* generate_navigator_js:  generates web navigator's config with keys
    identical keys used in navigator object

FIXME:
* add Edge, Safari and Opera support
* add random config i.e. windows is more common than linux

Specs:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent/Firefox
* http://msdn.microsoft.com/en-us/library/ms537503(VS.85).aspx
* https://developer.chrome.com/multidevice/user-agent
* http://www.javascriptkit.com/javatutors/navigator.shtml

Release history:
* https://en.wikipedia.org/wiki/Firefox_release_history
* https://en.wikipedia.org/wiki/Google_Chrome_release_history
* https://en.wikipedia.org/wiki/Internet_Explorer_version_history
* https://en.wikipedia.org/wiki/Android_version_history

Lists of user agents:
* http://www.useragentstring.com/
* http://www.user-agents.org/
* http://www.webapps-online.com/online-tools/user-agent-strings

"""
# pylint: enable=line-too-long

from random import choice, randint
from datetime import timedelta
from itertools import product

import six

from .warning import warn
# pylint: disable=unused-import
from .device import SMARTPHONE_DEV_IDS, TABLET_DEV_IDS
# pylint: enable=unused-import
from .error import InvalidOption
from .configuration import configuration

__all__ = ['generate_user_agent', 'generate_navigator',
           'generate_navigator_js']


def get_firefox_build():
    build_ver, date_from = choice(configuration.FIREFOX_VERSION)
    try:
        idx = configuration.FIREFOX_VERSION.index((build_ver, date_from))
        _, date_to = configuration.FIREFOX_VERSION[idx + 1]
    except IndexError:
        date_to = date_from + timedelta(days=1)
    sec_range = (date_to - date_from).total_seconds() - 1
    build_rnd_time = (date_from +
                      timedelta(seconds=randint(0, sec_range)))
    return build_ver, build_rnd_time.strftime('%Y%m%d%H%M%S')


def get_chrome_build():
    build = choice(configuration.CHROME_BUILD)
    return '%d.0.%d.%d' % (
        build[0],
        randint(build[1], build[2]),
        randint(0, 99),
    )


def get_ie_build():
    """
    Return random IE version as tuple
    (numeric_version, us-string component)

    Example: (8, 'MSIE 8.0')
    """
    return choice(configuration.IE_VERSION)


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
    build_range = range(*configuration.MACOSX_CHROME_BUILD_RANGE[ver])
    build = choice(build_range)
    mac_ver = ver.replace('.', '_') + '_' + str(build)
    return 'Macintosh; Intel Mac OS X %s' % mac_ver


def build_system_components(device_type, os_id, navigator_id):
    """
    For given os_id build random platform and oscpu
    components

    Returns dict {platform_version, platform, ua_platform, oscpu}

    platform_version is OS name used in different places
    ua_platform goes to navigator.platform
    platform is used in building navigator.userAgent
    oscpu goes to navigator.oscpu
    """

    if os_id == 'win':
        platform_version = choice(configuration.OS_PLATFORM['win'])
        cpu = choice(configuration.OS_CPU['win'])
        if cpu:
            platform = '%s; %s' % (platform_version, cpu)
        else:
            platform = platform_version
        res = {
            'platform_version': platform_version,
            'platform': platform,
            'ua_platform': platform,
            'oscpu': platform,
        }
    elif os_id == 'linux':
        cpu = choice(configuration.OS_CPU['linux'])
        platform_version = choice(configuration.OS_PLATFORM['linux'])
        platform = '%s %s' % (platform_version, cpu)
        res = {
            'platform_version': platform_version,
            'platform': platform,
            'ua_platform': platform,
            'oscpu': 'Linux %s' % cpu,
        }
    elif os_id == 'mac':
        cpu = choice(configuration.OS_CPU['mac'])
        platform_version = choice(configuration.OS_PLATFORM['mac'])
        platform = platform_version
        if navigator_id == 'chrome':
            platform = fix_chrome_mac_platform(platform)
        res = {
            'platform_version': platform_version,
            'platform': 'MacIntel',
            'ua_platform': platform,
            'oscpu': 'Intel Mac OS X %s' % platform.split(' ')[-1],
        }
    elif os_id == 'android':
        assert navigator_id in ('firefox', 'chrome')
        assert device_type in ('smartphone', 'tablet')
        platform_version = choice(configuration.OS_PLATFORM['android'])
        if navigator_id == 'firefox':
            if device_type == 'smartphone':
                ua_platform = '%s; Mobile' % platform_version
            elif device_type == 'tablet':
                ua_platform = '%s; Tablet' % platform_version
        elif navigator_id == 'chrome':
            device_id = choice(SMARTPHONE_DEV_IDS)
            ua_platform = 'Linux; %s; %s' % (platform_version, device_id)
        oscpu = 'Linux %s' % choice(configuration.OS_CPU['android'])
        res = {
            'platform_version': platform_version,
            'ua_platform': ua_platform,
            'platform': oscpu,
            'oscpu': oscpu,
        }
    return res


def build_app_components(os_id, navigator_id):
    """
    For given navigator_id build app features

    Returns dict {name, product_sub, vendor, build_version, build_id}
    """

    if navigator_id == 'firefox':
        build_version, build_id = get_firefox_build()
        if os_id in ('win', 'linux', 'mac'):
            geckotrail = '20100101'
        else:
            geckotrail = build_version
        res = {
            'name': 'Netscape',
            'product_sub': '20100101',
            'vendor': '',
            'build_version': build_version,
            'build_id': build_id,
            'geckotrail': geckotrail,
        }
    elif navigator_id == 'chrome':
        res = {
            'name': 'Netscape',
            'product_sub': '20030107',
            'vendor': 'Google Inc.',
            'build_version': get_chrome_build(),
            'build_id': None,
        }
    elif navigator_id == 'ie':
        num_ver, build_version, trident_version = get_ie_build()
        if num_ver >= 11:
            app_name = 'Netscape'
        else:
            app_name = 'Microsoft Internet Explorer'
        res = {
            'name': app_name,
            'product_sub': None,
            'vendor': '',
            'build_version': build_version,
            'build_id': None,
            'trident_version': trident_version,
        }
    return res


def get_option_choices(opt_name, opt_value, default_value, all_choices):
    """
    Generate possible choices for the option `opt_name`
    limited to `opt_value` value with default value
    as `default_value`
    """

    choices = []
    if isinstance(opt_value, six.string_types):
        choices = [opt_value]
    elif isinstance(opt_value, (list, tuple)):
        choices = list(opt_value)
    elif opt_value is None:
        choices = default_value
    else:
        raise InvalidOption('Option %s has invalid'
                            ' value: %s' % (opt_name, opt_value))
    if 'all' in choices:
        choices = all_choices
    for item in choices:
        if item not in all_choices:
            raise InvalidOption('Choices of option %s contains invalid'
                                ' item: %s' % (opt_name, item))
    return choices


def pick_config_ids(device_type, os, navigator):
    """
    Select one random pair (device_type, os_id, navigator_id) from
    all possible combinations matching the given os and
    navigator filters.

    :param os: allowed os(es)
    :type os: string or list/tuple or None
    :param navigator: allowed browser engine(s)
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    """

    if os is None:
        default_dev_types = ['desktop']
    else:
        default_dev_types = list(configuration.DEVICE_TYPE_OS.keys())
    dev_type_choices = get_option_choices(
        'device_type', device_type, default_dev_types,
        list(configuration.DEVICE_TYPE_OS.keys())
    )
    os_choices = get_option_choices('os', os, list(configuration.OS_NAVIGATOR.keys()),
                                    list(configuration.OS_NAVIGATOR.keys()))
    nav_choices = get_option_choices('navigator', navigator,
                                     list(configuration.NAVIGATOR_OS.keys()),
                                     list(configuration.NAVIGATOR_OS.keys()))

    variants = []
    for dev, os, nav in product(dev_type_choices, os_choices,
                                nav_choices):

        if (os in configuration.DEVICE_TYPE_OS[dev]
                and nav in configuration.DEVICE_TYPE_NAVIGATOR[dev]
                and nav in configuration.OS_NAVIGATOR[os]):
            variants.append((dev, os, nav))
    if not variants:
        raise InvalidOption('Options device_type, os and navigator'
                            ' conflicts with each other')
    device_type, os_id, navigator_id = choice(variants)

    assert os_id in configuration.OS_PLATFORM
    assert navigator_id in configuration.NAVIGATOR_OS
    assert device_type in configuration.DEVICE_TYPE_OS

    return device_type, os_id, navigator_id


def choose_ua_template(device_type, navigator_id, app):
    tpl_name = navigator_id
    if navigator_id == 'ie':
        tpl_name = ('ie_11' if app['build_version'] == 'MSIE 11.0'
                    else 'ie_less_11')
    if navigator_id == 'chrome':
        if device_type == 'smartphone':
            tpl_name = 'chrome_smartphone'
        if device_type == 'tablet':
            tpl_name = 'chrome_tablet'
    return configuration.USER_AGENT_TEMPLATE[tpl_name]


def build_navigator_app_version(os_id, navigator_id,
                                platform_version, user_agent):
    if navigator_id in ('chrome', 'ie'):
        assert user_agent.startswith('Mozilla/')
        app_version = user_agent.split('Mozilla/', 1)[1]
    elif navigator_id == 'firefox':
        if os_id == 'android':
            app_version = '5.0 (%s)' % platform_version
        else:
            os_token = {
                'win': 'Windows',
                'mac': 'Macintosh',
                'linux': 'X11',
            }[os_id]
            app_version = '5.0 (%s)' % os_token
    return app_version


def generate_navigator(os=None, navigator=None, platform=None,
                       device_type=None):
    """
    Generates web navigator's config

    :param os: limit list of oses for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"

    :return: User-Agent config
    :rtype: dict with keys (os, name, platform, oscpu, build_version,
                            build_id, app_version, app_name, app_code_name,
                            product, product_sub, vendor, vendor_sub,
                            user_agent)
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed platforms and navigators
    :raise InvalidOption: if any of passed options is invalid
    """

    if platform is not None:
        os = platform
        warn('The `platform` option is deprecated.'
             ' Use `os` option instead.', stacklevel=3)
    device_type, os_id, navigator_id = (
        pick_config_ids(device_type, os, navigator)
    )
    system = build_system_components(
        device_type, os_id, navigator_id)
    app = build_app_components(os_id, navigator_id)
    ua_template = choose_ua_template(
        device_type, navigator_id, app)
    user_agent = ua_template.format(system=system, app=app)
    app_version = build_navigator_app_version(
        os_id, navigator_id, system['platform_version'], user_agent)
    return {
        # ids
        'os_id': os_id,
        'navigator_id': navigator_id,
        # system components
        'platform': system['platform'],
        'oscpu': system['oscpu'],
        # app components
        'build_version': app['build_version'],
        'build_id': app['build_id'],
        'app_version': app_version,
        'app_name': app['name'],
        'app_code_name': 'Mozilla',
        'product': 'Gecko',
        'product_sub': app['product_sub'],
        'vendor': app['vendor'],
        'vendor_sub': '',
        # compiled user agent
        'user_agent': user_agent,
    }


def generate_user_agent(os=None, navigator=None, platform=None,
                        device_type=None):
    """
    Generates HTTP User-Agent header

    :param os: limit list of os for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    :return: User-Agent string
    :rtype: string
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed oses and navigators
    :raise InvalidOption: if any of passed options is invalid
    """
    return generate_navigator(os=os, navigator=navigator,
                              platform=platform,
                              device_type=device_type)['user_agent']


def generate_navigator_js(os=None, navigator=None, platform=None,
                          device_type=None):
    """
    Generates web navigator's config with keys corresponding
    to keys of `windows.navigator` JavaScript object.

    :param os: limit list of oses for generation
    :type os: string or list/tuple or None
    :param navigator: limit list of browser engines for generation
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    :return: User-Agent config
    :rtype: dict with keys (TODO)
    :raises InvalidOption: if could not generate user-agent for
        any combination of allowed oses and navigators
    :raise InvalidOption: if any of passed options is invalid
    """

    config = generate_navigator(os=os, navigator=navigator,
                                platform=platform,
                                device_type=device_type)
    return {
        'appCodeName': config['app_code_name'],
        'appName': config['app_name'],
        'appVersion': config['app_version'],
        'platform': config['platform'],
        'userAgent': config['user_agent'],
        'oscpu': config['oscpu'],
        'product': config['product'],
        'productSub': config['product_sub'],
        'vendor': config['vendor'],
        'vendorSub': config['vendor_sub'],
        'buildID': config['build_id'],
    }
