import json
import urllib
import urllib2
from datetime import datetime
from datetime import timedelta
import time
import ssl
import logging
import argparse

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

def retrieve_pagerduty_logs (day_to_retrieve, pagination_offset):

    start = day_to_retrieve.replace(hour=0, minute=0, second=0, microsecond=0)
    now = day_to_retrieve + timedelta(days=1)
    logging.info("Fetching pagerduty logs from {0} to {1}".format(start,now))
    # Get data from PagerDuty
    headers = {
            "Authorization" :"Token token=" + args.pagerduty_token,
            'Content-type': 'application/json'
        }
    data = {
        "since" : start.isoformat(),
        "until": now.isoformat(),
        "offset": pagination_offset,
        "is_overview": "false"
    }
    url = "https://api.pagerduty.com/log_entries?%s" % (urllib.urlencode(data))
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        logging.error("Error sending getting data from Pagerduty: {0} {1}".format(e.code, e.reason))

    the_page =  unicode(response.read(),errors='replace')
    page_json = json.loads(the_page)

    logging.debug(json.dumps(page_json))

    return page_json

def format_pagerduty_logs_for_splunk(pagerduty_logs):
    # Set the data in the right format for Splunk
    data = ''
    for (i, item) in enumerate(pagerduty_logs['log_entries']):

        # Convert the time
        eventTime = item['created_at']
        eventTime = datetime.strptime(eventTime, "%Y-%m-%dT%H:%M:%SZ")
        eventTime = int(time.mktime(eventTime.timetuple()))
        data += json.dumps({"event": item,"time":eventTime})

    logging.debug(json.dumps(data))
    return data

def push_data_to_splunk(data):

    # Trial splunk accounts use self-signed certs
    ssl_context = ssl._create_unverified_context()
    logging.info("Pushing data to splunk")
    headers = {
        "Authorization" :"Splunk " + args.splunk_token,
        'Content-type': 'application/json'
    }
    url = "https://input-" + args.splunk_instance_id + ".cloud.splunk.com:8088/services/collector/event"

    req = urllib2.Request(url, data, headers=headers)
    try:
        response = urllib2.urlopen(req,context = ssl_context)
    except urllib2.HTTPError, e:
        logging.error("Error sending data to Splunk: {0} {1}".format(e.code, e.reason))

        return False
    the_page =  unicode(response.read(),errors='replace')
    page_json = json.loads(the_page)

    logging.debug(json.dumps(page_json))

    return page_json

# Function to push all pagerduty logs from a given day to splunk
def push_pagerduty_to_splunk(day_to_push):

    more_logs = True
    pagination_offset = 0

    while more_logs:

        logging.info("Fetching logs from {0} days ago (record offset {1})".format(day_offset, pagination_offset))
        pagerduty_logs = retrieve_pagerduty_logs(day_to_push, pagination_offset)
        more_logs = pagerduty_logs['more']

        # If there are no results, skip to the next day
        if len(pagerduty_logs['log_entries']) == 0:
            logging.info("There are no logs for this day/page, continuing to next day)")
            more_logs = False
            continue

        # Push the data we've got to Splunk
        splunk_input = format_pagerduty_logs_for_splunk(pagerduty_logs)
        splunk_result = push_data_to_splunk(splunk_input)

        # If there are more results, increase our pagination offset
        if more_logs:
            pagination_offset = pagination_offset + pagerduty_logs['limit']
            logging.info("There are more logs for this day! Increasing pagination offset to {0})".format(
                pagination_offset
            ))

for day_offset in range(int(args.start),int(args.end)):
    now = datetime.now()
    cur_day = now + timedelta(days=day_offset*-1)

    push_pagerduty_to_splunk(cur_day)
