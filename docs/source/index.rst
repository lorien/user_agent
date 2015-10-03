user_agent library documentation
================================

The user_agent is a library for:

* generating extended user agent config that could be used in JS environment
* generating simple user-agent string that could be used as content of User-Agent HTTP header

Supported platforms: windows, linux,  mac.

Supported browsers: chrome, firefox.

.. py:module:: user_agent

.. autofunction:: generate_user_agent

Returns a string like::

    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36


.. autofunction:: generate_navigator

Returns a dict like:

.. code:: python

    {'appversion': '5.0',
     'name': 'chrome',
     'os': 'win',
     'oscpu': 'Windows NT 10.0; WOW64',
     'platform': 'Win32',
     'user_agent': 'Mozilla/5.0 ... Safari/537.36',
     'version': '39.0.2172.16'}


.. toctree::
   :maxdepth: 2


External links
==============

* Specifications:
    * https://developer.mozilla.org/en-US/docs/Web/HTTP/Gecko_user_agent_string_reference
    * http://msdn.microsoft.com/en-us/library/ms537503(VS.85).aspx
    * https://developer.chrome.com/multidevice/user-agent

* Lists of user agents:
    * http://www.useragentstring.com/
    * http://www.user-agents.org/ 


* Browser Release history:
    * https://en.wikipedia.org/wiki/Firefox_release_history
    * https://en.wikipedia.org/wiki/Google_Chrome_release_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
