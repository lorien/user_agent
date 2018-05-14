#!/usr/bin/env python
# pylint: disable=missing-docstring

from __future__ import absolute_import

import pytest
from voluptuous import MultipleInvalid
from user_agent import (generate_user_agent,
                        generate_navigator,
                        load_file_configuration)


@pytest.mark.last
def test_external_file_configuration():
    load_file_configuration("test/data/unique_configuration.json")
    for _ in range(50):
        agent = generate_user_agent(os='linux')
        assert 'golden snitch' in agent.lower()

        navigator = generate_navigator(os='linux')
        assert 'golden snitch' in navigator['platform'].lower()

        agent = generate_user_agent(os='win')
        assert 'nimbus' in agent.lower()

        agent = generate_user_agent(os='mac')
        assert '42' in agent.lower()

        agent = generate_user_agent(navigator='firefox')
        assert '4.0' in agent.lower()

        agent = generate_user_agent(navigator='chrome')
        assert '4242' in agent.lower()

        agent = generate_user_agent(navigator='ie')
        assert 'quaffle' in agent.lower()


def test_no_file():
    with pytest.raises(IOError):
        load_file_configuration("test/data/configuration.json")
        generate_user_agent()


def test_wrong_format():
    with pytest.raises(MultipleInvalid):
        load_file_configuration("test/data/wrong_format_configuration.json")
        generate_user_agent()
