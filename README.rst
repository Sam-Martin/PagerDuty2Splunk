PagerDuty2Splunk |pypiversion| |travisbuild|
=======================




This module allows you to take logs from PagerDuty and push them into Splunk for analysis.
https://github.com/Sam-Martin/PagerDuty2Splunk

----

Installation
--------------
Provided you have Python installed, you can simply run:

.. code-block::

   pip install pagerduty2splunk

Examples
--------
**Relative:** Push logs between yesterday and three days ago to Splunk:

.. code-block::

   pagerduty2splunk --log=INFO --start=1 --end=3 --splunk-token=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX  --splunk-instance-id=prd-X-XXXXX --pagerduty-token=XXX-XXXXXXXXXXXXXXXX

**Absolute**: Push logs from 2016-01-01 to 2016-01-05 to Splunk:

.. code-block::

   pagerduty2splunk --log=INFO --start=2016-01-01 --end=2015-01-05 --splunk-token=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX  --splunk-instance-id=prd-X-XXXXX --pagerduty-token=XXX-XXXXXXXXXXXXXXXX


Arguments
----------

* **splunk-instance-id** is the subdomain of your Splunk instance in Splunk cloud

* **splunk-token** is the token of your  `HTTP Event Collector`_.

* **pagerduty-token** is your **V2** API token (see `Generating an API Key`_ for more details).

.. _HTTP Event Collector: http://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector
.. _Generating an API Key: https://support.pagerduty.com/hc/en-us/articles/202829310-Generating-an-API-Key
.. |pypiversion| image:: https://img.shields.io/pypi/v/pagerduty2splunk.svg
.. |travisbuild| image:: https://travis-ci.org/Sam-Martin/PagerDuty2Splunk.svg?branch=master
