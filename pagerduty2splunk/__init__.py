import json
import urllib
import urllib2
from datetime import datetime
from datetime import timedelta
import time
import ssl
import logging
import argparse

from .main import push_pagerduty_to_splunk

parser = argparse.ArgumentParser(description='Get logs from PagerDuty and push them to Splunk.')
parser.add_argument('-l','--log-level', help='Log level',required=False)
parser.add_argument('-s','--start', help='Number of days ago to start from',required=False, default=1)
parser.add_argument('-e','--end', help='Number of days ago to stop at',required=False, default=2)
parser.add_argument('-st','--splunk-token', help='The Splunk HTTP Event Collector token you created', required=True)
parser.add_argument('-si','--splunk-instance-id', help='The instance id (subdomain) of your Splunk Cloud instance',required=True)
parser.add_argument('-p','--pagerduty-token', help='The V2 API token you created for your Splunk account',required=True)
args = parser.parse_args()

numeric_log_level = getattr(logging, args.log_level.upper())
logging.basicConfig(level=numeric_log_level)

for day_offset in range(int(args.start),int(args.end)):
    now = datetime.now()
    cur_day = now + timedelta(days=day_offset*-1)

    push_pagerduty_to_splunk(cur_day)
