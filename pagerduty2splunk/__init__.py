from datetime import datetime
from datetime import timedelta
import logging
import argparse

from .main import push_pagerduty_to_splunk

# Define Arguments
def parse_args(args):
    parser = argparse.ArgumentParser(description='Get logs from PagerDuty and push them to Splunk.')
    parser.add_argument('-l','--log-level', help='Log level',required=False)
    parser.add_argument('-s','--start', help='Number of days ago to start from',required=False, default=1)
    parser.add_argument('-e','--end', help='Number of days ago to stop at',required=False, default=2)
    parser.add_argument('-st','--splunk-token', help='The Splunk HTTP Event Collector token you created', required=True)
    parser.add_argument('-si','--splunk-instance-id', help='The instance id (subdomain) of your Splunk Cloud instance',required=True)
    parser.add_argument('-p','--pagerduty-token', help='The V2 API token you created for your Splunk account',required=True)

    args = parser.parse_args()
    # Set log level
    numeric_log_level = getattr(logging, args.log_level.upper())
    logging.basicConfig(level=numeric_log_level)

    return args



def validate(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return True

def main():
    args = parse_args(sys.argv[1:])

    # Check if we're doing dates relative to now in days
    if args.start.isdigit() & args.end.isdigit():

        for day_offset in range(int(args.start),int(args.end)):
            now = datetime.now()
            cur_day = now + timedelta(days=day_offset*-1)

            push_pagerduty_to_splunk(cur_day, args.pagerduty_token, args.splunk_instance_id, args.splunk_token)

    # Otherwise if it's a date, do that
    elif validate(args.start) & validate(args.end):

        # Parse into proper date objects
        start = datetime.strptime(args.start, '%Y-%m-%d')
        end = datetime.strptime(args.end, '%Y-%m-%d')
        delta = end - start

        for day_offset in range(0,delta.days):
            cur_day = start + timedelta(days=day_offset)
            push_pagerduty_to_splunk(cur_day, args.pagerduty_token, args.splunk_instance_id, args.splunk_token)
    else:
        logger.error("Start and End dates must be either numeric or date formatted YYYY-MM-DD")
