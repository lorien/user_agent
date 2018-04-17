# -*- coding: utf-8 -*-
# pylint: disable=line-too-long
"""
This module is for storing different configuration
It has possibility to load configuration from external place (e.g. string, file)

Usage::

    load configuration from json file
    >>> load_file_configuration("./external_config.json")

    or load from string in json format
    >>> load_configuration("{...}")

Example of file format:
    {
  "OS_PLATFORM" : {
        "win": [
            "Windows NT 5.1",
            ...
            "Windows NT 10.0"
        ],
        "mac": [
            "Macintosh; Intel Mac OS X 10.9",
            ...
            "Macintosh; Intel Mac OS X 10.13"
        ],
        "linux": [
            "X11; Linux",
            "X11; Ubuntu; Linux"
        ],
        "android": [
            "Android 5.0",
            ...
            "Android 7.1.1"
        ]
    },

  "FIREFOX_VERSION": [
    ["53.0", "2017-4-19"],
    ...
    ["59.0", "2018-3-13"]
  ],
  "CHROME_BUILD": [
    [60, 3112, 3112],
    ...
    [65, 3325, 3325]
  ],
  "IE_VERSION": [
    [8, "MSIE 8.0", "4.0"],
    ...
    [11, "MSIE 11.0", "7.0"]
  ],
  "MACOSX_CHROME_BUILD_RANGE": {
    "10.9": [0, 5],
    ...
    "10.13": [0, 3]
  }
}

"""
# pylint: enable=line-too-long
from datetime import datetime
import json

from voluptuous import (Schema, Required,
                        Length, All, ExactSequence,
                        MultipleInvalid, SchemaError,
                        ALLOW_EXTRA, Coerce)

DATE_FORMAT = '%Y-%m-%d'

__all__ = ['Configuration',
           'load_configuration',
           'load_file_configuration']


class Configuration(object):
    # Default values

    DEVICE_TYPE_OS = {
        'desktop': ('win', 'mac', 'linux'),
        'smartphone': ('android',),
        'tablet': ('android',),
    }

    OS_DEVICE_TYPE = {
        'win': ('desktop',),
        'linux': ('desktop',),
        'mac': ('desktop',),
        'android': ('smartphone', 'tablet'),
    }

    DEVICE_TYPE_NAVIGATOR = {
        'desktop': ('chrome', 'firefox', 'ie'),
        'smartphone': ('firefox', 'chrome'),
        'tablet': ('firefox', 'chrome'),
    }

    NAVIGATOR_DEVICE_TYPE = {
        'ie': ('desktop',),
        'chrome': ('desktop', 'smartphone', 'tablet'),
        'firefox': ('desktop', 'smartphone', 'tablet'),
    }

    OS_PLATFORM = {
        'win': (
            'Windows NT 5.1',  # Windows XP
            'Windows NT 6.1',  # Windows 7
            'Windows NT 6.2',  # Windows 8
            'Windows NT 6.3',  # Windows 8.1
            'Windows NT 10.0',  # Windows 10
        ),
        'mac': (
            'Macintosh; Intel Mac OS X 10.9',
            'Macintosh; Intel Mac OS X 10.10',
            'Macintosh; Intel Mac OS X 10.11',
            'Macintosh; Intel Mac OS X 10.12'
        ),
        'linux': (
            'X11; Linux',
            'X11; Ubuntu; Linux',
        ),
        'android': (
            'Android 4.4',  # 2013-10-31
            'Android 4.4.1',  # 2013-12-05
            'Android 4.4.2',  # 2013-12-09
            'Android 4.4.3',  # 2014-06-02
            'Android 4.4.4',  # 2014-06-19
            'Android 5.0',  # 2014-11-12
            'Android 5.0.1',  # 2014-12-02
            'Android 5.0.2',  # 2014-12-19
            'Android 5.1',  # 2015-03-09
            'Android 5.1.1',  # 2015-04-21
            'Android 6.0',  # 2015-10-05
            'Android 6.0.1',  # 2015-12-07
            # 'Android 7.0', # 2016-08-22
            # 'Android 7.1', # 2016-10-04
            # 'Android 7.1.1', # 2016-12-05
        ),
    }
    OS_CPU = {
        'win': (
            '',  # 32bit
            'Win64; x64',  # 64bit
            'WOW64',  # 32bit process on 64bit system
        ),
        'linux': (
            'i686',  # 32bit
            'x86_64',  # 64bit
            'i686 on x86_64',  # 32bit process on 64bit system
        ),
        'mac': (
            '',
        ),
        'android': (
            'armv7l',  # 32bit
            'armv8l',  # 64bit
        ),
    }

    OS_NAVIGATOR = {
        'win': ('chrome', 'firefox', 'ie'),
        'mac': ('firefox', 'chrome'),
        'linux': ('chrome', 'firefox'),
        'android': ('firefox', 'chrome'),
    }

    NAVIGATOR_OS = {
        'chrome': ('win', 'linux', 'mac', 'android'),
        'firefox': ('win', 'linux', 'mac', 'android'),
        'ie': ('win',),
    }

    FIREFOX_VERSION = (
        ('45.0', datetime(2016, 3, 8)),
        ('46.0', datetime(2016, 4, 26)),
        ('47.0', datetime(2016, 6, 7)),
        ('48.0', datetime(2016, 8, 2)),
        ('49.0', datetime(2016, 9, 20)),
        ('50.0', datetime(2016, 11, 15)),
        ('51.0', datetime(2017, 1, 24)),
    )

    CHROME_BUILD = (
        (49, 2623, 2660),  # 2016-03-02
        (50, 2661, 2703),  # 2016-04-13
        (51, 2704, 2742),  # 2016-05-25
        (52, 2743, 2784),  # 2016-07-20
        (53, 2785, 2839),  # 2016-08-31
        (54, 2840, 2882),  # 2016-10-12
        (55, 2883, 2923),  # 2016-12-01
        (56, 2924, 2986),  # 2016-12-01
    )

    IE_VERSION = (
        # (numeric ver, string ver, trident ver) # release year
        (8, 'MSIE 8.0', '4.0'),  # 2009
        (9, 'MSIE 9.0', '5.0'),  # 2011
        (10, 'MSIE 10.0', '6.0'),  # 2012
        (11, 'MSIE 11.0', '7.0'),  # 2013
    )

    USER_AGENT_TEMPLATE = {
        'firefox': (
            'Mozilla/5.0'
            ' ({system[ua_platform]}; rv:{app[build_version]})'
            ' Gecko/{app[geckotrail]}'
            ' Firefox/{app[build_version]}'
        ),
        'chrome': (
            'Mozilla/5.0'
            ' ({system[ua_platform]}) AppleWebKit/537.36'
            ' (KHTML, like Gecko)'
            ' Chrome/{app[build_version]} Safari/537.36'
        ),
        'chrome_smartphone': (
            'Mozilla/5.0'
            ' ({system[ua_platform]}) AppleWebKit/537.36'
            ' (KHTML, like Gecko)'
            ' Chrome/{app[build_version]} Mobile Safari/537.36'
        ),
        'chrome_tablet': (
            'Mozilla/5.0'
            ' ({system[ua_platform]}) AppleWebKit/537.36'
            ' (KHTML, like Gecko)'
            ' Chrome/{app[build_version]} Safari/537.36'
        ),
        'ie_less_11': (
            'Mozilla/5.0'
            ' (compatible; {app[build_version]}; {system[ua_platform]};'
            ' Trident/{app[trident_version]})'
        ),
        'ie_11': (
            'Mozilla/5.0'
            ' ({system[ua_platform]}; Trident/{app[trident_version]};'
            ' rv:11.0) like Gecko'
        ),
    }

    MACOSX_CHROME_BUILD_RANGE = {
        # https://en.wikipedia.org/wiki/MacOS#Release_history
        '10.8': (0, 8),
        '10.9': (0, 5),
        '10.10': (0, 5),
        '10.11': (0, 6),
        '10.12': (0, 2)
    }


def load_configuration(external_config):
    """
       Load json from external_config string, validate and convert it,
       set parameters to config object

       :param external_config: values for versions of OS_PLATFORM,
       FIREFOX_VERSION, CHROME_BUILD, IE_VERSION
       and MACOSX_CHROME_BUILD_RANGE
       :type external_config: string in json format
    """

    external_config = json.loads(external_config)

    validate_external_configuration(external_config)

    Configuration.OS_PLATFORM = external_config['OS_PLATFORM']
    Configuration.FIREFOX_VERSION = list_to_tuple(
        external_config['FIREFOX_VERSION'])
    Configuration.CHROME_BUILD = external_config['CHROME_BUILD']
    Configuration.IE_VERSION = external_config['IE_VERSION']
    Configuration.MACOSX_CHROME_BUILD_RANGE = (
        external_config['MACOSX_CHROME_BUILD_RANGE'])


def load_file_configuration(json_file_path):
    with open(json_file_path, encoding='utf-8') as data_file:
        load_configuration(data_file)


# --- Convertation functions ---


def date_hook(value):
    try:
        return datetime.strptime(value, DATE_FORMAT)
    except ValueError:
        return value


def list_to_tuple(list_of_lists):
    return tuple(tuple(list(map(date_hook, x))) for x in list_of_lists)


# --- Validation functions ---


def date(fmt=DATE_FORMAT):
    return lambda v: datetime.strptime(v, fmt)


SCHEMA = Schema({
    Required("OS_PLATFORM"): Schema({
        Required('win'): All([All(Coerce(str), Length(min=1))], Length(min=1)),
        Required('mac'): All([All(Coerce(str), Length(min=1))], Length(min=1)),
        Required('linux'): All([All(Coerce(str), Length(min=1))],
                               Length(min=1)),
        Required('android'): All([All(Coerce(str), Length(min=1))],
                                 Length(min=1))
    }),
    Required('FIREFOX_VERSION'): All([
        All(ExactSequence([Coerce(str), date()]),
            Length(min=2, max=2))], Length(min=1)),
    Required('CHROME_BUILD'): All([All([Coerce(int)],
                                       Length(min=3, max=3))],
                                  Length(min=1)),
    Required('IE_VERSION'): All([ExactSequence([Coerce(int),
                                                Coerce(str), Coerce(str)])],
                                Length(min=1)),
    Required('MACOSX_CHROME_BUILD_RANGE'): Schema({str: All(
        ExactSequence([Coerce(int), Coerce(int)]),
        Length(min=2, max=2))}, extra=ALLOW_EXTRA)
})


def validate_external_configuration(external_config):
    # Validation according to schema
    SCHEMA(external_config)

    # External validation:

    # Length FIREFOX_VERSION and IE_VERSION lists
    for browser, version_length in (
            {'FIREFOX_VERSION': 2, 'IE_VERSION': 3}.items()):
        for version in external_config[browser]:
            try:
                assert len(version) == version_length
            except AssertionError:
                raise MultipleInvalid(errors=[
                    SchemaError("Too much values in {}".format(browser))
                ])

    # MACOSX_CHROME_BUILD_RANGE versions should be present in OS_PLATFORM
    mac_platforms = list(
        map(lambda platform_string: platform_string.split('OS X ')[1],
            external_config['OS_PLATFORM']['mac']))
    for version_key in external_config['MACOSX_CHROME_BUILD_RANGE'].keys():
        try:
            assert version_key in mac_platforms
        except AssertionError:
            raise MultipleInvalid(errors=[
                SchemaError("There's no {} version of mac OSX "
                            "chrome build in OS_PLATFORM.mac"
                            .format(version_key))
            ])

    # Length of range of MACOSX_CHROME_BUILD
    for build_range in external_config['MACOSX_CHROME_BUILD_RANGE'].values():
        try:
            assert len(build_range) == 2
        except AssertionError:
            raise MultipleInvalid(errors=[
                SchemaError("Too much values in "
                            "MACOSX_CHROME_BUILD_RANGE field, in list {}"
                            .format(build_range))
            ])
