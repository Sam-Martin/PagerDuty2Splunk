PagerDuty2Splunk
=======================

This module allows you to take logs from PagerDuty and push them into Splunk for analysis.
https://github.com/Sam-Martin/PagerDuty2Splunk

----

Example
-------

.. code-block::

   pagerduty2splunk --log=INFO --start=0 --end=3 --splunk-token=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX  --splunk-instance-id=prd-X-XXXXX --pagerduty-token=XXX-XXXXXXXXXXXXXXXX

* **splunk-instance-id** is the subdomain of your Splunk instance in Splunk cloud

* **splunk-token** is the token of your  `HTTP Event Collector`_.

* **pagerduty-token** is your **V2** API token (see `Generating an API Key`_ for more details).

.. _HTTP Event Collector: http://docs.splunk.com/Documentation/Splunk/latest/Data/UsetheHTTPEventCollector
.. _Generating an API Key: https://support.pagerduty.com/hc/en-us/articles/202829310-Generating-an-API-Key
