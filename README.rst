==========
user_agent
==========

.. image:: https://travis-ci.org/lorien/grab.png?branch=master
    :target: https://travis-ci.org/lorien/grab?branch=master

.. image:: https://img.shields.io/pypi/dm/user_agent.svg
    :target: https://pypi.python.org/pypi/user_agent

.. image:: https://img.shields.io/pypi/v/user_agent.svg
    :target: https://pypi.python.org/pypi/user_agent


What is for user_agent library?
-------------------------------

Well, it is for generating content of content of User-Agent header.


Usage Example
-------------

.. code:: python

    >>> from user_agent import generate_user_agent
    >>> generate_user_agent(platform='linux')
    'Mozilla/5.0 (X11; Ubuntu; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36'


Installation
------------

Use pip::

.. code:: bash

    $ pip install -U user_agent


Contribution
============

Use github to submit bug,fix or wish request: https://github.com/lorien/user_agent/issues
