==========
user_agent
==========

.. image:: https://travis-ci.org/lorien/user_agent.png?branch=master
    :target: https://travis-ci.org/lorien/user_agent?branch=master

.. image:: https://img.shields.io/pypi/dm/user_agent.svg
    :target: https://pypi.python.org/pypi/user_agent

.. image:: https://img.shields.io/pypi/v/user_agent.svg
    :target: https://pypi.python.org/pypi/user_agent


What is user_agent module for?
-------------------------------

This module is for generating random, valid web navigator's configs & User-Agent HTTP headers.


Usage Example
-------------

.. code:: python

    >>> from user_agent import generate_user_agent, generate_navigator
    >>> generate_user_agent()
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:40.0) Gecko/20100101 Firefox/40.0'
    >>> generate_user_agent(platform=('mac', 'linux'))
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:36.0) Gecko/20100101 Firefox/36.0'
    >>> generate_navigator(platform='win', navigator='chrome')
    {'appversion': '5.0',
     'name': 'chrome',
     'os': 'win',
     'oscpu': 'Windows NT 10.0; WOW64',
     'platform': 'Win32',
     'user_agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2172.16 Safari/537.36',
     'version': '39.0.2172.16'}


Installation
------------

Use pip:

.. code:: shell

    $ pip install -U user_agent


Contribution
============

Use github to submit bug,fix or wish request: https://github.com/lorien/user_agent/issues

