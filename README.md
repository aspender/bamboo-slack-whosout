# bamboo-slack-whosout

An AWS Lambda function to query the BambooHR who's out API and post to slack.

This will query the [Time Off API](https://www.bamboohr.com/api/documentation/time_off.php) to obtain the list of people within your organisation who have any form of time-off booked for the current day. It will then post one or more of three messages to the configured Slack channel:

If today is a configured holiday: `Today is: Christmas Day! :confetti_ball:`
If nodbody is out: `Nobody is out today! :tada:`
If people are out: `Who's out today: Bob Smith, Alice Jones`

## Requirements

You need to configure the code with:

* Details of your BambooHR account, including the domain (uk, us), your account name.
* A valid BambooHR API key
* A valid Slack incoming webhook
* The name of the Slack channel to send to.

You can then configure the Lambda function to run on a Cloudwatch scheduled cron event.

NOTE: Be careful if using a personal BambooHR API key as this will allow API access to all of the data allowed for the user it is associated with. You could inadvertently allow anybody who can view your Lambda code in AWS to see your salary, which I guesss is fine if you [work for Buffer](https://open.buffer.com/introducing-open-salaries-at-buffer-including-our-transparent-formula-and-all-individual-salaries/) :)