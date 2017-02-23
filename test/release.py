from __future__ import absolute_import
import re

import user_agent


def test_changelog():
    """
    Parse changelog and ensure that it contains
    * unreleased version younger than release date
    * release version has a date
    """
    re_date = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    ver_dates = {}
    ver_history = []
    for line in open('CHANGELOG.md'):
        if line.startswith('## ['):
            ver = line.split('[')[1].split(']')[0]
            date = line.split('-', 1)[1].strip().lower()
            ver_dates[ver] = date
            ver_history.append(ver)
    release = user_agent.__version__
    print(ver_dates)
    print(ver_history)
    assert 'unreleased' not in ver_dates[release]
    assert re_date.match(ver_dates[release])
    assert ver_history.index(release) == 1
