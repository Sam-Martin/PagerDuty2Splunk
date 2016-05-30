import sys
sys.path.append('pagerduty2splunk/')
import unittest
from mock import patch, Mock
from datetime import datetime
from main import retrieve_pagerduty_logs, format_pagerduty_logs_for_splunk, push_data_to_splunk

import json

urllib_mocks = ["""{
"log_entries": [
{
"id": "Q02JTSNZWHSEKV",
"type": "trigger_log_entry",
"summary": "Triggered through the API",
"self": "https://api.pagerduty.com/log_entries/Q02JTSNZWHSEKV?incident_id=PT4KHLK",
"html_url": "https://subdomain.pagerduty.com/incidents/PT4KHLK/log_entries/Q02JTSNZWHSEKV",
"created_at": "2015-11-07T00:14:20Z",
"agent": {
"id": "PIJ90N7",
"type": "generic_email_reference",
"summary": "My Mail Service",
"self": "https://api.pagerduty.com/services/PIJ90N7",
"html_url": "https://subdomain.pagerduty.com/services/PIJ90N7"
},
"channel": {
"type": "api"
},
"incident": {
"id": "PT4KHLK",
"type": "incident_reference",
"summary": "The server is on fire.",
"self": "https://api.pagerduty.com/incidents/PT4KHLK",
"html_url": "https://subdomain.pagerduty.com/incidents/PT4KHLK"
},
"teams": [
{
  "id": "PQ9K7I8",
  "type": "team_reference",
  "summary": "Engineering",
  "self": "https://api.pagerduty.com/teams/PQ9K7I8",
  "html_url": "https://subdomain.pagerduty.com/teams/PQ9K7I8"
}
],
"contexts": [],
"event_details": {
"description": "Tasks::SFDCValidator - PD_Data__c - duplicates"
}
}
],
"limit": 1,
"offset": 0,
"total": null,
"more": false
}""",
"""{"text": "Success", "code": 0}"""]

formatted_for_splunk = """{"event": {"event_details": {"description": "Tasks::SFDCValidator - PD_Data__c - duplicates"}, "contexts": [], "created_at": "2015-11-07T00:14:20Z", "teams": [{"self": "https://api.pagerduty.com/teams/PQ9K7I8", "type": "team_reference", "id": "PQ9K7I8", "html_url": "https://subdomain.pagerduty.com/teams/PQ9K7I8", "summary": "Engineering"}], "html_url": "https://subdomain.pagerduty.com/incidents/PT4KHLK/log_entries/Q02JTSNZWHSEKV", "agent": {"self": "https://api.pagerduty.com/services/PIJ90N7", "type": "generic_email_reference", "id": "PIJ90N7", "html_url": "https://subdomain.pagerduty.com/services/PIJ90N7", "summary": "My Mail Service"}, "id": "Q02JTSNZWHSEKV", "incident": {"self": "https://api.pagerduty.com/incidents/PT4KHLK", "type": "incident_reference", "id": "PT4KHLK", "html_url": "https://subdomain.pagerduty.com/incidents/PT4KHLK", "summary": "The server is on fire."}, "summary": "Triggered through the API", "type": "trigger_log_entry", "self": "https://api.pagerduty.com/log_entries/Q02JTSNZWHSEKV?incident_id=PT4KHLK", "channel": {"type": "api"}}, "time": 1446855260}"""


@patch('main.urllib2.urlopen')
class TestStringMethods(unittest.TestCase):
    def test_retrieve_pagerduty_logs(self, mock_urlopen):
        a = Mock()
        a.read.side_effect = [urllib_mocks[0]]
        mock_urlopen.return_value = a
        result = retrieve_pagerduty_logs(datetime.now(),0, "test")
        self.assertEqual(result, json.loads(urllib_mocks[0]))

    def test_format_pagerduty_logs_for_splunk(self, mock_urlopen):
        result = format_pagerduty_logs_for_splunk(json.loads(urllib_mocks[0]))
        self.assertEqual(result, formatted_for_splunk)

    def test_push_data_to_splunk(self, mock_urlopen):
        a = Mock()
        a.read.side_effect = [urllib_mocks[1]]
        mock_urlopen.return_value = a
        result = push_data_to_splunk(formatted_for_splunk,"instanceID", "token")
        self.assertEqual(result, json.loads(urllib_mocks[1]))

if __name__ == '__main__':
    unittest.main()
