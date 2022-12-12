# Documentation for user\_agent package


[![Test Status](https://github.com/lorien/user_agent/actions/workflows/test.yml/badge.svg)](https://github.com/lorien/user_agent/actions/workflows/test.yml)
[![Code Quality](https://github.com/lorien/user_agent/actions/workflows/check.yml/badge.svg)](https://github.com/lorien/user_agent/actions/workflows/test.yml)
[![Type Check](https://github.com/lorien/user_agent/actions/workflows/mypy.yml/badge.svg)](https://github.com/lorien/user_agent/actions/workflows/mypy.yml)
[![Documentation Status](https://readthedocs.org/projects/user_agent/badge/?version=latest)](http://user-agent.readthedocs.org)


## What is user\_agent module for?

This module is for generating random, valid web user agents:

* content of "User-Agent" HTTP headers
* content of `window.navigator` JavaScript object


## Usage Example

```
>>> from user_agent import generate_user_agent, generate_navigator
>>> from pprint import pprint
>>> generate_user_agent()
'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'
>>> generate_user_agent(os=('mac', 'linux'))
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0'
>>> pprint(generate_navigator())
{'app_code_name': 'Mozilla',
 'app_name': 'Netscape',
 'appversion': '5.0',
 'name': 'firefox',
 'os': 'linux',
 'oscpu': 'Linux i686 on x86_64',
 'platform': 'Linux i686 on x86_64',
 'user_agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
 'version': '41.0'}
>>> pprint(generate_navigator_js())
{'appCodeName': 'Mozilla',
 'appName': 'Netscape',
 'appVersion': '38.0',
 'platform': 'MacIntel',
 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) Gecko/20100101 Firefox/38.0'}
```


## Installation

Run `pip install -U user_agent`


## Documentation

Documentation is available at http://user-agent.readthedocs.org


## Contribution

Use github to submit bug,fix or wish request: https://github.com/lorien/user\_agent/issues
