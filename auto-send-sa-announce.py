# Import the request http library to talk to Sermon Audio
import requests
# Import Beautiful Soup class from Beautiful Soup 4 library
from bs4 import BeautifulSoup
# Import the regular expression library
import re 
# Import the json library
import json 
# Import the smtplib library
import smtplib
# Import EmailMessage class from email.message 
from email.message import EmailMessage
# Open the configuration file
try:
	config_file=open('config.json')
except:
	exit('Configuration file config.json not found!')
# Loading JSON format
config=json.load(config_file)
# Open file sermons.json 
sermon_file=open('sermons.json')
# Defining sermons 
sermons=json.load(sermon_file)
# Print message to user
print('Fetching sermon page from SermonAudio ...')
# Get html page from Sermon Audio server 
request_page = requests.get('https://www.sermonaudio.com/search.asp?SourceOnly=true&currSection=sermonssource&keyword=' + config['churchKey'] + '&mediatype=MP4')
# Print server status code to user
print('Server responded with status code=' + str(request_page.status_code))
# Print message about writing html file to user
print('Writing html to output.html file ...')
# Create file to write the response to
output = open("output.html", "w", encoding="utf-8")
# Write the html page requested to the file 
output.write(request_page.text)
# Use Beautiful Soup to parse the html response
soup=BeautifulSoup(request_page.text, 'html.parser')
# Get tables which are of the local-sermonbar class 
tables=soup.find_all('table', class_='local-sermonbar')
if not tables:
	exit('Local sermon-bar tables cannot be found')
# Iterate through all the local-sermonbar tables 
sids=[]
messages=[]
for table in tables:
	# Look for popup video link
	refs=table.find_all('a', onclick="return popupWindowVideo(this.href);")
	# If no popup then continue
	if not refs:
		print('Popup Window Video is not found')
		continue
	# Find SID within popup link using regular expression
	result=re.search('https://www\.sermonaudio\.com/playpopupvideo\.asp\?SID=([0-9]*)', refs[0]['href'])
	# If SID not found continue
	if not result:
		print('SID cannot be found')
		continue 
	# If this is a new SID then print the info out
	if result.group(1) not in sermons:
			# Get the title of this sermon table
			title=table.find_all(string=re.compile(config['sermonsRegex']))
			# If title not found continue
			if not title:
				print('Sermon title not found SID=' + result.group(1))
				continue
			# Print Announcement 
			print(config['announcement'] + ' Announcement: '+ title[0][0:-3] + ' now available\n')
			# Print the popup video
			print(refs[0]['href'] + '\n')
			# Append messages
			messages.append(config['announcement'] + ' Announcement: ' + title[0][0:-3] + ' now available\n' + refs[0]['href'])
	# Append Sids after validations
	sids.append(result.group(1))
if messages:
		print('Sending new sermons to {} ...'.format(config['recipient']))
		subject = ''
		msg = EmailMessage()
		msg['Subject'] = ''
		msg['From'] = config['sender']
		msg['To'] = config['recipient']

		s = smtplib.SMTP_SSL(config['server'])
		s.login(config['sender'], config['token'])
		for message in messages:
			msg.set_content(message)
			s.send_message(msg)
		s.quit()

# Create sermons.json file with SIDs
json_file =  open("sermons.json", "w") 
# Write SIDs to file
json.dump(sids, json_file)