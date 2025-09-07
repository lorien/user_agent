"""Generation random, valid HTTP User-Agent header and web navgator JS object.

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
# from __future__ import annotations

import typing
from datetime import datetime, timedelta
from itertools import product
from random import SystemRandom

import pytz
from six.moves.collections_abc import (  # pylint: disable=import-error,unused-import
    Sequence,
)

from .device import SMARTPHONE_DEV_IDS
from .error import InvalidOption
from .warning import warn

# pylint: enable=line-too-long


__all__ = ["generate_navigator", "generate_navigator_js", "generate_user_agent"]

IE_NETSCAPE_VERSION = 11
randomizer = SystemRandom()
DEVICE_TYPE_OS = {
    "desktop": ("win", "mac", "linux"),
    "smartphone": ("android",),
    "tablet": ("android",),
}
OS_DEVICE_TYPE = {
    "win": ("desktop",),
    "linux": ("desktop",),
    "mac": ("desktop",),
    "android": ("smartphone", "tablet"),
}
DEVICE_TYPE_NAVIGATOR = {
    "desktop": ("chrome", "firefox", "ie"),
    "smartphone": ("firefox", "chrome"),
    "tablet": ("firefox", "chrome"),
}
NAVIGATOR_DEVICE_TYPE = {
    "ie": ("desktop",),
    "chrome": ("desktop", "smartphone", "tablet"),
    "firefox": ("desktop", "smartphone", "tablet"),
}
OS_PLATFORM = {
    "win": (
        "Windows NT 5.1",  # Windows XP
        "Windows NT 6.1",  # Windows 7
        "Windows NT 6.2",  # Windows 8
        "Windows NT 6.3",  # Windows 8.1
        "Windows NT 10.0",  # Windows 10
    ),
    "mac": (
        "Macintosh; Intel Mac OS X 10.8",
        "Macintosh; Intel Mac OS X 10.9",
        "Macintosh; Intel Mac OS X 10.10",
        "Macintosh; Intel Mac OS X 10.11",
        "Macintosh; Intel Mac OS X 10.12",
    ),
    "linux": (
        "X11; Linux",
        "X11; Ubuntu; Linux",
    ),
    "android": (
        "Android 4.4",  # 2013-10-31
        "Android 4.4.1",  # 2013-12-05
        "Android 4.4.2",  # 2013-12-09
        "Android 4.4.3",  # 2014-06-02
        "Android 4.4.4",  # 2014-06-19
        "Android 5.0",  # 2014-11-12
        "Android 5.0.1",  # 2014-12-02
        "Android 5.0.2",  # 2014-12-19
        "Android 5.1",  # 2015-03-09
        "Android 5.1.1",  # 2015-04-21
        "Android 6.0",  # 2015-10-05
        "Android 6.0.1",  # 2015-12-07
        # 'Android 7.0', # 2016-08-22
        # 'Android 7.1', # 2016-10-04
        # 'Android 7.1.1', # 2016-12-05
    ),
}
OS_CPU = {
    "win": (
        "",  # 32bit
        "Win64; x64",  # 64bit
        "WOW64",  # 32bit process on 64bit system
    ),
    "linux": (
        "i686",  # 32bit
        "x86_64",  # 64bit
        "i686 on x86_64",  # 32bit process on 64bit system
    ),
    "mac": ("",),
    "android": (
        "armv7l",  # 32bit
        "armv8l",  # 64bit
    ),
}
OS_NAVIGATOR = {
    "win": ("chrome", "firefox", "ie"),
    "mac": ("firefox", "chrome"),
    "linux": ("chrome", "firefox"),
    "android": ("firefox", "chrome"),
}
NAVIGATOR_OS = {
    "chrome": ("win", "linux", "mac", "android"),
    "firefox": ("win", "linux", "mac", "android"),
    "ie": ("win",),
}
FIREFOX_VERSION = [
    ("45.0", datetime(2016, 3, 8, tzinfo=pytz.utc)),
    ("46.0", datetime(2016, 4, 26, tzinfo=pytz.utc)),
    ("47.0", datetime(2016, 6, 7, tzinfo=pytz.utc)),
    ("48.0", datetime(2016, 8, 2, tzinfo=pytz.utc)),
    ("49.0", datetime(2016, 9, 20, tzinfo=pytz.utc)),
    ("50.0", datetime(2016, 11, 15, tzinfo=pytz.utc)),
    ("51.0", datetime(2017, 1, 24, tzinfo=pytz.utc)),
]  # type: list[tuple[str, datetime]]

# Top chrome builds from website access log
# for september, october 2020
CHROME_BUILD = """
80.0.3987.132
80.0.3987.149
80.0.3987.99
81.0.4044.117
81.0.4044.138
83.0.4103.101
83.0.4103.106
83.0.4103.96
84.0.4147.105
84.0.4147.111
84.0.4147.125
84.0.4147.135
84.0.4147.89
85.0.4183.101
85.0.4183.102
85.0.4183.120
85.0.4183.121
85.0.4183.127
85.0.4183.81
85.0.4183.83
86.0.4240.110
86.0.4240.111
86.0.4240.114
86.0.4240.183
86.0.4240.185
86.0.4240.75
86.0.4240.78
86.0.4240.80
86.0.4240.96
86.0.4240.99
""".strip().splitlines()  # type: list[str]

IE_VERSION = [
    # (numeric ver, string ver, trident ver) # release year
    (8, "MSIE 8.0", "4.0"),  # 2009
    (9, "MSIE 9.0", "5.0"),  # 2011
    (10, "MSIE 10.0", "6.0"),  # 2012
    (11, "MSIE 11.0", "7.0"),  # 2013
]  # type: list[tuple[int, str, str]]
USER_AGENT_TEMPLATE = {
    "firefox": (
        "Mozilla/5.0"
        " ({system[ua_platform]}; rv:{app[build_version]})"
        " Gecko/{app[geckotrail]}"
        " Firefox/{app[build_version]}"
    ),
    "chrome": (
        "Mozilla/5.0"
        " ({system[ua_platform]}) AppleWebKit/537.36"
        " (KHTML, like Gecko)"
        " Chrome/{app[build_version]} Safari/537.36"
    ),
    "chrome_smartphone": (
        "Mozilla/5.0"
        " ({system[ua_platform]}) AppleWebKit/537.36"
        " (KHTML, like Gecko)"
        " Chrome/{app[build_version]} Mobile Safari/537.36"
    ),
    "chrome_tablet": (
        "Mozilla/5.0"
        " ({system[ua_platform]}) AppleWebKit/537.36"
        " (KHTML, like Gecko)"
        " Chrome/{app[build_version]} Safari/537.36"
    ),
    "ie_less_11": (
        "Mozilla/5.0"
        " (compatible; {app[build_version]}; {system[ua_platform]};"
        " Trident/{app[trident_version]})"
    ),
    "ie_11": (
        "Mozilla/5.0"
        " ({system[ua_platform]}; Trident/{app[trident_version]};"
        " rv:11.0) like Gecko"
    ),
}


MACOSX_CHROME_BUILD_RANGE = {
    # https://en.wikipedia.org/wiki/MacOS#Release_history
    "10.8": (0, 8),
    "10.9": (0, 5),
    "10.10": (0, 5),
    "10.11": (0, 6),
    "10.12": (0, 2),
}  # type: dict[str, tuple[int, int]]


def get_firefox_build():
    # type: () -> tuple[str, str]
    build_ver, date_from = randomizer.choice(FIREFOX_VERSION)
    try:
        idx = FIREFOX_VERSION.index((build_ver, date_from))
        _, date_to = FIREFOX_VERSION[idx + 1]
    except IndexError:
        date_to = date_from + timedelta(days=1)
    sec_range = (date_to - date_from).total_seconds() - 1
    build_rnd_time = date_from + timedelta(
        seconds=randomizer.randint(0, int(sec_range))
    )
    return build_ver, build_rnd_time.strftime("%Y%m%d%H%M%S")


def get_chrome_build():
    # type: () -> str
    return randomizer.choice(CHROME_BUILD)


def get_ie_build():
    # type: () -> tuple[int, str, str]
    """Return random IE version as tuple (numeric_version, us-string component).

    Example: (8, 'MSIE 8.0')
    """
    return randomizer.choice(IE_VERSION)


def fix_chrome_mac_platform(platform):
    # type: (str) -> str
    """Fix chrome version on mac OS.

    Chrome on Mac OS adds minor version number and uses underscores instead
    of dots. E.g. platform for Firefox will be: 'Intel Mac OS X 10.11'
    but for Chrome it will be 'Intel Mac OS X 10_11_6'.

    :param platform: - string like "Macintosh; Intel Mac OS X 10.8"
    :return: platform with version number including minor number and formatted
    with underscores, e.g. "Macintosh; Intel Mac OS X 10_8_2"
    """
    ver = platform.split("OS X ")[1]
    build_range = range(*MACOSX_CHROME_BUILD_RANGE[ver])
    build = randomizer.choice(build_range)
    mac_ver = ver.replace(".", "_") + "_" + str(build)
    return "Macintosh; Intel Mac OS X {}".format(mac_ver)


def build_system_components(device_type, os_id, navigator_id):
    # type: (str, str, str) -> dict[str, str]
    """Build random platform and oscpu components for given parameters.

    Returns dict {platform_version, platform, ua_platform, oscpu}

    platform_version is OS name used in different places
    ua_platform goes to navigator.platform
    platform is used in building navigator.userAgent
    oscpu goes to navigator.oscpu
    """
    assert os_id in {"win", "linux", "mac", "android"}
    if os_id == "win":
        platform_version = randomizer.choice(OS_PLATFORM["win"])
        cpu = randomizer.choice(OS_CPU["win"])
        platform = "{}; {}".format(platform_version, cpu) if cpu else platform_version
        return {
            "platform_version": platform_version,
            "platform": platform,
            "ua_platform": platform,
            "oscpu": platform,
        }
    if os_id == "linux":
        cpu = randomizer.choice(OS_CPU["linux"])
        platform_version = randomizer.choice(OS_PLATFORM["linux"])
        platform = "{} {}".format(platform_version, cpu)
        return {
            "platform_version": platform_version,
            "platform": platform,
            "ua_platform": platform,
            "oscpu": "Linux {}".format(cpu),
        }
    if os_id == "mac":
        cpu = randomizer.choice(OS_CPU["mac"])
        platform_version = randomizer.choice(OS_PLATFORM["mac"])
        platform = platform_version
        if navigator_id == "chrome":
            platform = fix_chrome_mac_platform(platform)
        return {
            "platform_version": platform_version,
            "platform": "MacIntel",
            "ua_platform": platform,
            "oscpu": "Intel Mac OS X {}".format(platform.split(" ")[-1]),
        }
    # os_id could be only "android" here
    assert navigator_id in {"firefox", "chrome"}
    assert device_type in {"smartphone", "tablet"}
    platform_version = randomizer.choice(OS_PLATFORM["android"])
    if navigator_id == "firefox":
        if device_type == "smartphone":
            ua_platform = "{}; Mobile".format(platform_version)
        elif device_type == "tablet":
            ua_platform = "{}; Tablet".format(platform_version)
        else:
            ua_platform = "TODO"
    elif navigator_id == "chrome":
        device_id = randomizer.choice(SMARTPHONE_DEV_IDS)
        ua_platform = "Linux; {}; {}".format(platform_version, device_id)
    else:
        ua_platform = "TODO"
    oscpu = "Linux {}".format(randomizer.choice(OS_CPU["android"]))
    return {
        "platform_version": platform_version,
        "ua_platform": ua_platform,
        "platform": oscpu,
        "oscpu": oscpu,
    }


def build_app_components(os_id, navigator_id):
    # type: (str, str) -> dict[str, None | str]
    """Build app features for given os and navigator.

    Returns dict {name, product_sub, vendor, build_version, build_id}
    """
    assert navigator_id in {"firefox", "chrome", "ie"}
    if navigator_id == "firefox":
        build_version, build_id = get_firefox_build()
        geckotrail = "20100101" if os_id in {"win", "linux", "mac"} else build_version
        return {
            "name": "Netscape",
            "product_sub": "20100101",
            "vendor": "",
            "build_version": build_version,
            "build_id": build_id,
            "geckotrail": geckotrail,
        }
    if navigator_id == "chrome":
        return {
            "name": "Netscape",
            "product_sub": "20030107",
            "vendor": "Google Inc.",
            "build_version": get_chrome_build(),
            "build_id": None,
        }
    # navigator_id could be only "ie" here
    num_ver, build_version, trident_version = get_ie_build()
    app_name = (
        "Netscape" if num_ver >= IE_NETSCAPE_VERSION else "Microsoft Internet Explorer"
    )
    return {
        "name": app_name,
        "product_sub": None,
        "vendor": "",
        "build_version": build_version,
        "build_id": None,
        "trident_version": trident_version,
    }


# TODO: I have no idea what this function does
def get_option_choices(
    opt_name,  # type: str
    opt_value,  # type: None | str | Sequence[str]
    default_value,  # type: list[str]
    all_choices,  # type: list[str]
):
    # type: (...) -> list[str]
    """Generate something.

    Long uninformative description: Generate possible choices for the
    option `opt_name` limited to `opt_value` value with default value
    as `default_value`
    """
    choices = []
    if isinstance(opt_value, str):
        choices = [opt_value]
    elif isinstance(
        opt_value, typing.Sequence  # pylint: disable=deprecated-typing-alias
    ):
        choices = list(opt_value)
    elif opt_value is None:
        choices = default_value
    else:
        raise InvalidOption(
            "Option {} has invalid value: {}".format(opt_name, opt_value)
        )
    if "all" in choices:
        choices = all_choices
    for item in choices:
        if item not in all_choices:
            raise InvalidOption(
                "Choices of option {} contains invalid item: {}".format(opt_name, item)
            )
    return choices


def pick_config_ids(
    device_type=None,  # type: None | str | list[str]
    os=None,  # type: None | str | Sequence[str]
    navigator=None,  # type: None | str | Sequence[str]
):
    # type: (...) -> tuple[str, str, str]
    """Select one item from all possible combinations of (device, os, navigator) items.

    :param os: allowed os(es)
    :type os: string or list/tuple or None
    :param navigator: allowed browser engine(s)
    :type navigator: string or list/tuple or None
    :param device_type: limit possible oses by device type
    :type device_type: str or list/tuple or None, possible values:
        "desktop", "smartphone", "tablet", "all"
    """
    default_dev_types = ["desktop"] if os is None else list(DEVICE_TYPE_OS.keys())
    dev_type_choices = get_option_choices(
        "device_type", device_type, default_dev_types, list(DEVICE_TYPE_OS.keys())
    )
    os_choices = get_option_choices(
        "os", os, list(OS_NAVIGATOR.keys()), list(OS_NAVIGATOR.keys())
    )
    nav_choices = get_option_choices(
        "navigator", navigator, list(NAVIGATOR_OS.keys()), list(NAVIGATOR_OS.keys())
    )

    variants = []
    for iter_dev, iter_os, iter_nav in product(
        dev_type_choices, os_choices, nav_choices
    ):
        if (
            iter_os in DEVICE_TYPE_OS[iter_dev]
            and iter_nav in DEVICE_TYPE_NAVIGATOR[iter_dev]
            and iter_nav in OS_NAVIGATOR[iter_os]
        ):
            variants.append((iter_dev, iter_os, iter_nav))
    if not variants:
        raise InvalidOption(
            "Options device_type, os and navigator conflicts with each other"
        )
    device_type, os_id, navigator_id = randomizer.choice(variants)

    assert os_id in OS_PLATFORM
    assert navigator_id in NAVIGATOR_OS
    assert device_type in DEVICE_TYPE_OS

    return device_type, os_id, navigator_id


def choose_ua_template(
    device_type,  # type: str
    navigator_id,  # type: str
    app,  # type: dict[str, None | str]
):
    # type: (...) -> str
    tpl_name = navigator_id
    if navigator_id == "ie":
        tpl_name = "ie_11" if app["build_version"] == "MSIE 11.0" else "ie_less_11"
    if navigator_id == "chrome":
        if device_type == "smartphone":
            tpl_name = "chrome_smartphone"
        if device_type == "tablet":
            tpl_name = "chrome_tablet"
    return USER_AGENT_TEMPLATE[tpl_name]


def build_navigator_app_version(os_id, navigator_id, platform_version, user_agent):
    # type: (str, str, str, str) -> str
    if navigator_id == "firefox":
        if os_id == "android":
            return "5.0 ({})".format(platform_version)
        os_token = {
            "win": "Windows",
            "mac": "Macintosh",
            "linux": "X11",
        }[os_id]
        return "5.0 ({})".format(os_token)
    # here navigator_id could be only "chrome" and "ie"
    assert user_agent.startswith("Mozilla/")
    return user_agent.split("Mozilla/", 1)[1]


def generate_navigator(
    os=None,  # type: None | str
    navigator=None,  # type: None | str
    platform=None,  # type: None | str
    device_type=None,  # type: None | str
):
    # type: (...) -> dict[str, None | str]
    """Generate web navigator's config.

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
        warn(
            "The `platform` option is deprecated. Use `os` option instead.",
            stacklevel=3,
        )
    device_type, os_id, navigator_id = pick_config_ids(device_type, os, navigator)
    system = build_system_components(device_type, os_id, navigator_id)
    app = build_app_components(os_id, navigator_id)
    ua_template = choose_ua_template(device_type, navigator_id, app)
    user_agent = ua_template.format(system=system, app=app)
    app_version = build_navigator_app_version(
        os_id, navigator_id, system["platform_version"], user_agent
    )
    return {
        # ids
        "os_id": os_id,
        "navigator_id": navigator_id,
        # system components
        "platform": system["platform"],
        "oscpu": system["oscpu"],
        # app components
        "build_version": app["build_version"],
        "build_id": app["build_id"],
        "app_version": app_version,
        "app_name": app["name"],
        "app_code_name": "Mozilla",
        "product": "Gecko",
        "product_sub": app["product_sub"],
        "vendor": app["vendor"],
        "vendor_sub": "",
        # compiled user agent
        "user_agent": user_agent,
    }


def generate_user_agent(
    os=None,  # type: None | str
    navigator=None,  # type: None | str
    platform=None,  # type: None | str
    device_type=None,  # type: None | str
):
    # type: (...) -> str
    """Generate HTTP User-Agent header.

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
    config = generate_navigator(
        os=os, navigator=navigator, platform=platform, device_type=device_type
    )
    assert config["user_agent"] is not None
    return config["user_agent"]


def generate_navigator_js(
    os=None,  # type: None | str
    navigator=None,  # type: None | str
    platform=None,  # type: None | str
    device_type=None,  # type: None | str
):
    # type: (...) -> dict[str, None | str]
    """Generate config for `windows.navigator` JavaScript object.

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
    config = generate_navigator(
        os=os, navigator=navigator, platform=platform, device_type=device_type
    )
    return {
        "appCodeName": config["app_code_name"],
        "appName": config["app_name"],
        "appVersion": config["app_version"],
        "platform": config["platform"],
        "userAgent": config["user_agent"],
        "oscpu": config["oscpu"],
        "product": config["product"],
        "productSub": config["product_sub"],
        "vendor": config["vendor"],
        "vendorSub": config["vendor_sub"],
        "buildID": config["build_id"],
    }
