import json
import logging
import base64
import datetime

from urllib2 import Request, urlopen, URLError, HTTPError
from datetime import datetime
from datetime import timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#
# Configure these variables for your environment
#

# The domain of your BambooHR account (uk or us)
BAMBOO_DOMAIN = "uk"

# Your BambooHR account name (the first part of your BambooHR url)
BAMBOO_ACCOUNT = "REDACTED"

# Your BambooHR API Key - note that if you use a personal API key generated from the
# BambooHR API and then run this code on AWS you are exposing all of the BambooHR data
# you can access to anybody who can view your Lambda code! Contact BambooHR support
# to get a specific API key for this purpose.
BAMBOO_API_KEY = "REDACTED"

# The incoming slack webhook to send messages to
SLACK_WEB_HOOK = "REDACTED"

# The slack channel to send messages to
SLACK_CHANNEL = "general"

# Do not modify below here

base64string = base64.encodestring('%s:%s' % (BAMBOO_API_KEY, "blah")).replace('\n', '')

bamboodomains = {
  "uk" : "api.bamboohr.co.uk",
  "us" : "api.bamboohr.com"
}

def whosout(today):
  out = []  
  bamboorequest = Request("https://{0}/api/gateway.php/{1}/v1/time_off/whos_out/?filter=off&end={2}".format(bamboodomains[BAMBOO_DOMAIN], BAMBOO_ACCOUNT, today.strftime("%Y-%m-%d")))

  bamboorequest.add_header("Authorization", "Basic %s" % base64string)
  bamboorequest.add_header("Accept", "application/json")
  try:
    result = urlopen(bamboorequest)
    return json.loads(result.read())   
  except HTTPError as e:
    logger.error("Request failed: %d %s", e.code, e.reason)
  except URLError as e:
    logger.error("Server connection failed: %s", e.reason)
  return names

def posttoslack(text):
  slack_message = {
    "attachments": [
      {
        "fallback": "Who's out?",
        "text": text,
        "mrkdwn_in": ["text"],
        "username": "bamboo-bot",
        "fields": [],
        "color": "#F3F300"
      }
    ],
    "channel": SLACK_CHANNEL
  }

  req = Request(SLACK_WEB_HOOK, json.dumps(slack_message))
  try:
    response = urlopen(req)
    response.read()
    logger.info("Message posted to %s", slack_message['channel'])
  except HTTPError as e:
    logger.error("Request failed: %d %s", e.code, e.reason)
  except URLError as e:
    logger.error("Server connection failed: %s", e.reason)


def lambda_handler(event, context):
  today = datetime.now()

  out = whosout(today)

  if out:
    names = []
    for who in out:
      if who.get("type") == "holiday":
        posttoslack("*Today is:* {} :confetti_ball:".format(who.get("name")))
      else:
        names.append(who.get("name"))

    if names:
      text = "*Who's out today:* {}".format(', '.join(names))
      posttoslack(text)
  else:
    posttoslack("Nobody is out today! :tada:")
