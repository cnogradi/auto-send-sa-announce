# Automatically Send Sermon Audio Announcements

The purpose of this script is to poll a church's Sermon Audio video page to determine if any new sermons have been published; and, if so, to publish the new sermons discovered to a single email recipient.  The script could be used to text a person and notify them of new sermons posted if the recipient email is a mobile phone number and carrier combination (<phone-number>@vtext.com for Verizon).

The script expects the existance of a config.json file from which to load necessary configuration information such as Sermon Audio church key, sender email and token, recipient email, ...  A sample config.json.template is available as an example.  Please rename to config.json and fill with appropriate values.

The script keeps track of previously processed sermons for which notifications have already been sent in a sermons.json file.  Note that the first time the script is run, it will send all sermons to the recipient.

A Jenkinsfile is provided to easily integrate the script into Jenkins to allow it to run periodically if a change is detected using a URL Trigger (URL Trigger and Config File Provider plugins are required).  Make sure your church key is configured as a Global or Agent environment variable.

The script was used to teach a programming class with my children by way of practical example.  This script is written to instruct general programming and is therefore not Pythonic.

# Opportunities for improvement:
- handle multiple recipients
- make Pythonic/apply linter
