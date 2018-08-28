from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import getpass
import imaplib
import os
import datetime
import time

import csv
from tabulate import tabulate
#https://github.com/deerishi/uwpythonworkshop/blob/master/ebay.py
#https://stackoverflow.com/questions/348630/how-can-i-download-all-emails-with-attachments-from-gmail
#https://stackoverflow.com/questions/38275467/send-table-as-an-email-body-not-attachment-in-python
#https://pymotw.com/2/imaplib/#uploading-messages
# python celery 

def getdate():
	now = datetime.datetime.now()
	return now.strftime('%B') + ' ' + str(now.day + 4) + ' ' + str(now.year)

def getMIME():
	text = '''
	Hello fine folks, \n
	It's time to sign up for Food Not Bombs once again :)\n Please sign up for the tasks that you're planning to do on the sign up sheet: https://docs.google.com/spreadsheets/d/1rOeV_fEl_1wLedUWv44LzcK3VeLCGiL-UmRRyu-8KIg/edit#gid=1078847430
	
	Here is a table of the usual tasks: 
	{table}
	
	Take care, 
	Auto the Email Robot
	'''

	html = '''
	<html><body>
	<p>Hello fine folks, </p>
	<p>It's time to sign up for Food Not Bombs once again :)</p>
	<p>Please sign up for the tasks that you're planning to do <a href="https://docs.google.com/spreadsheets/d/1rOeV_fEl_1wLedUWv44LzcK3VeLCGiL-UmRRyu-8KIg/edit#gid=1078847430">on the sign-up sheet!</a></p><br>
	<p>Here is a table of the usual tasks:</p>
	{table}

	<p>Take care, <br>
	Auto the Email Robot<br><br>
	PS: I am a robot written by Stacy Gaikovaia. Please email stacygaikovaia@gmail.com if I am making mistakes or if you have any suggestions for improvements</p>
	</body></html>
	'''
	with open('table.log') as tab:
		reader = csv.reader(tab)
		data = list(reader)

	test = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
	html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

	return MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
	
def main():
	usr = 'fnb.kitchener'
	passwd = getpass.getpass('Enter Password')

	serv = imaplib.IMAP4_SSL('imap.gmail.com')
	serv.login(usr, passwd)
	draft_dir = serv.select('[Gmail]/Drafts')

	new_message = getMIME()
	new_message['Subject'] = 'Food Not Bombs Sign Up Reminder (' + getdate() + ')'
	new_message['To'] = 'fnb@lists.wpirg.org'
	new_message['From'] = usr + '@gmail.com'

	serv.append('[Gmail]/Drafts', '',imaplib.Time2Internaldate(time.time()), str(new_message))



if __name__ == '__main__':
	print getdate()
	main()
