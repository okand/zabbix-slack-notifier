#! /usr/bin/env python

import sys
import requests
import json


# basic settings
webhook_url = 'https://hooks.slack.com/services/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
zabbix_url = 'https://<ip or domain>/zabbix/'
username = 'zabbix'


# data from zabbix
zabbix_to = sys.argv[1]
zabbix_subject = sys.argv[2]
zabbix_body = sys.argv[3]


# splitting the message body
splitstring = zabbix_body.split(",,")


# selecting the pieces
host_name = splitstring[0]
status = splitstring[1]
trigger_id = splitstring[2]
trigger_name = splitstring[3]
trigger_description = splitstring[4]
trigger_severity = splitstring[5]
event_id = splitstring[6]
event_date = splitstring[7]
event_time = splitstring[8]


# make a link
zabbix_link = zabbix_url + "tr_events.php?triggerid=" + trigger_id + "&eventid=" + event_id


# join event date and time
event_combined = event_date + " " + event_time


# make fallback string
fallback = host_name + " - " + trigger_name + " - " + status


# select color and emoji
if status == "OK":
  color = "#7bd795"
  icon_emoji = ":ok_hand:"
elif trigger_severity == "Information":
  color = "#799af8"
  icon_emoji = ":information_source:"
elif trigger_severity == "Warning":
  color = "#f8c96c"
  icon_emoji = ":warning:"
elif trigger_severity == "Average":
  color = "#f4a366"
  icon_emoji = ":exclamation:"
elif trigger_severity == "High":
  color = "#dc7c61"
  icon_emoji = ":bangbang:"
elif trigger_severity == "Disaster":
  color = "#d6625e"
  icon_emoji = ":fire:"
else:
  color = "#9aa9b2"
  icon_emoji = ":grey_question:"


# make json
message_to_slack = json.dumps({"text": zabbix_subject,"channel": zabbix_to,"username": username,"icon_emoji": icon_emoji,"attachments": [{"color": color,"fallback": fallback,"pretext": fallback,"author_name": host_name,"title": trigger_name,"title_link": zabbix_link,"text": trigger_description,"fields": [{"title": "Status","value": status,"short": True},{"title": "Severity","value": trigger_severity,"short": True},{"title": "Time","value": event_combined,"short": True},{"title": "EventID","value": event_id,"short": True}]}]})


# some tests
#f = open('/tmp/myfile.txt', 'w')
#f.write(message_to_slack)
#f.close()

#print(message_to_slack)


# send to slack
response = requests.post(
  webhook_url, data=message_to_slack,
  headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
  raise ValueError(
    'Request to slack returned an error %s, the response is:\n%s'
    % (response.status_code, response.text)
  )

