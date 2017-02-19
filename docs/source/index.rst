user_agent library documentation
================================

The user_agent is a library for:

* generating extended user agent config that could be used in JS environment
* generating simple user-agent string that could be used as content of User-Agent HTTP header

Supported platforms: windows, linux,  mac.

Supported browsers: chrome, firefox, ie.

.. py:module:: user_agent

.. autofunction:: generate_user_agent

Returns a string like::

    Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36


.. autofunction:: generate_navigator

Returns a dict like:

.. code:: python

    {'app_code_name': 'Mozilla',
     'app_name': 'Netscape',
     'app_version': '5.0 (Windows)',
     'build_id': '20170124100044',
     'build_version': '51.0',
     'navigator_id': 'firefox',
     'os_id': 'win',
     'oscpu': 'Windows NT 6.2',
     'platform': 'Windows NT 6.2',
     'product': 'Gecko',
     'product_sub': '20100101',
     'user_agent': 'Mozilla/5.0 (Windows NT 6.2; rv:51.0) Gecko/20100101 '
                   'Firefox/51.0',
     'vendor': '',
     'vendor_sub': ''}

.. autofunction:: generate_navigator_js

Returns a dict like:

.. code:: python

    {'appCodeName': 'Mozilla',
     'appName': 'Netscape',
     'appVersion': '5.0 (Macintosh; Intel Mac OS X 10_8_1) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/54.0.2840.93 Safari/537.36',
     'buildID': None,
     'oscpu': 'Intel Mac OS X 10_8_1',
     'platform': 'Macintosh; Intel Mac OS X 10_8_1',
     'product': 'Gecko',
     'productSub': '20030107',
     'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.93 '
                  'Safari/537.36',
     'vendor': 'Google Inc.',
     'vendorSub': ''}


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
