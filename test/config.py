#!/usr/bin/env python
# pylint: disable=missing-docstring

import pytest
from user_agent import configuration
from voluptuous import MultipleInvalid


def test_json_configuration_valid():
    configuration.load_external_configuration(
        ''' {
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
    }'''
    )
    assert len(configuration.CHROME_BUILD) == 2
    assert len(configuration.FIREFOX_VERSION) == 2
    assert len(configuration.IE_VERSION) == 2
    assert len(configuration.MACOSX_CHROME_BUILD_RANGE) == 2


def test_json_configuration_key_missing():
    # Should contain OS_PLATFORM key

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'OS_PLATFORM' in str(excinfo.value)


def test_json_configuration_not_enough_length():
    # Should not contain empty lists

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'win' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'FIREFOX_VERSION' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'CHROME_BUILD' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'IE_VERSION' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'CHROME_BUILD' in str(excinfo.value)


def test_json_configuration_wrong_order():
    # Should contain right order of parameters

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'FIREFOX_VERSION' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'IE_VERSION' in str(excinfo.value)


def test_json_configuration_extra_parameters():
    # Should contain specific quantity of parameters

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'FIREFOX_VERSION' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'CHROME_BUILD' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'IE_VERSION' in str(excinfo.value)

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert 'MACOSX_CHROME_BUILD_RANGE' in str(excinfo.value)


def test_json_configuration_macos_build_not_in_platform():
    # MACOSX_CHROME_BUILD_RANGE should contain only values that correspond to versions in platform

    with pytest.raises(MultipleInvalid) as excinfo:
        configuration.load_external_configuration(
            ''' {
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
        }'''
        )
    assert '10.10' in str(excinfo.value)

