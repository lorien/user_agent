#!/usr/bin/env python
# pylint: disable=missing-docstring

from __future__ import absolute_import
import pytest
from voluptuous import MultipleInvalid
from user_agent import (Configuration,
                        load_configuration)


def test_json_configuration_valid():
    load_configuration(
        """ {
        "OS_PLATFORM" : {
            "win": [
                "Windows NT 5.1",
                "Windows NT 10.0"
            ],
            "mac": [
                "Macintosh; Intel Mac OS X 10.9",
                "Macintosh; Intel Mac OS X 10.13"
            ],
            "linux": [
                "X11; Linux",
                "X11; Ubuntu; Linux"
            ],
            "android": [
                "Android 5.0",
                "Android 7.1.1"
            ]
        },
         "FIREFOX_VERSION": [
            ["53.0", "2017-4-19"],
            ["59.0", "2018-3-13"]
        ],
        "CHROME_BUILD": [
            [60, 3112, 3112],
            [65, 3325, 3325]
        ],
        "IE_VERSION": [
            [8, "MSIE 8.0", "4.0"],
            [11, "MSIE 11.0", "7.0"]
        ],
        "MACOSX_CHROME_BUILD_RANGE": {
            "10.9": [0, 5],
            "10.13": [0, 3]
        }
    }""")

    assert len(Configuration.CHROME_BUILD) == 2, \
        "New values wasn't set to CHROME_BUILD"
    assert len(Configuration.FIREFOX_VERSION) == 2, \
        "New values wasn't set to FIREFOX_VERSION"
    assert len(Configuration.IE_VERSION) == 2, \
        "New values wasn't set to IE_VERSION"
    assert len(Configuration.MACOSX_CHROME_BUILD_RANGE) == 2, \
        "New values wasn't set to MACOSX_CHROME_BUILD_RANGE"


def test_json_configuration_key_missing():
    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """{
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "OS_PLATFORM" in str(excinfo.value), \
        "Should contain OS_PLATFORM key"


def test_json_configuration_not_enough_length():
    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """{
            "OS_PLATFORM" : {
                "win": [],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "win" in str(excinfo.value), \
        "Should contain empty list for OS_PLATFORM.win"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "FIREFOX_VERSION" in str(excinfo.value), \
        "Should contain empty list for FIREFOX_VERSION"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "CHROME_BUILD" in str(excinfo.value), \
        "Should contain empty list for CHROME_BUILD"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "IE_VERSION" in str(excinfo.value), \
        "Should contain empty list for IE_VERSION"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": []
            }
        }"""
        )
    assert "CHROME_BUILD" in str(excinfo.value), \
        "Should contain empty list fot CHROME_BUILD"


def test_json_configuration_wrong_order():
    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["2017-4-19", "53.0"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "FIREFOX_VERSION" in str(excinfo.value), \
        "Should contain right order of parameters for FIREFOX_VERSION"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                ["MSIE 8.0", 8, "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "IE_VERSION" in str(excinfo.value), \
        "Should contain right order of parameters for IE_VERSION"


def test_json_configuration_extra_parameters():
    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19", "8745"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "FIREFOX_VERSION" in str(excinfo.value), \
        "Should contain specific quantity of parameters for FIREFOX_VERSION"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112, 8745]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "CHROME_BUILD" in str(excinfo.value), \
        "Should contain specific quantity of parameters for CHROME_BUILD"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0", 8745]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5]
            }
        }"""
        )
    assert "IE_VERSION" in str(excinfo.value), \
        "Should contain specific quantity of parameters for IE_VERSION"

    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 5.1",
                    "Windows NT 10.0"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9",
                    "Macintosh; Intel Mac OS X 10.13"
                ],
                "linux": [
                    "X11; Linux",
                    "X11; Ubuntu; Linux"
                ],
                "android": [
                    "Android 5.0",
                    "Android 7.1.1"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"],
                ["59.0", "2018-3-13"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112],
                [65, 3325, 3325]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"],
                [11, "MSIE 11.0", "7.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.9": [0, 5, 8745],
                "10.13": [0, 3]
            }
        }"""
        )
    assert "MACOSX_CHROME_BUILD_RANGE" in str(excinfo.value), \
        "Should contain specific quantity of parameters for " \
        "MACOSX_CHROME_BUILD_RANGE"


def test_json_configuration_macos_build_not_in_platform():
    with pytest.raises(MultipleInvalid) as excinfo:
        load_configuration(
            """ {
            "OS_PLATFORM" : {
                "win": [
                    "Windows NT 10.0"
                ],
                "mac": [
                    "Macintosh; Intel Mac OS X 10.9"
                ],
                "linux": [
                    "X11; Linux"
                ],
                "android": [
                    "Android 5.0"
                ]
            },
             "FIREFOX_VERSION": [
                ["53.0", "2017-4-19"]
            ],
            "CHROME_BUILD": [
                [60, 3112, 3112]
            ],
            "IE_VERSION": [
                [8, "MSIE 8.0", "4.0"]
            ],
            "MACOSX_CHROME_BUILD_RANGE": {
                "10.10": [0, 3]
            }
        }"""
        )
    assert "10.10" in str(excinfo.value), \
        "MACOSX_CHROME_BUILD_RANGE should contain only values" \
        " that correspond to versions in platform"
