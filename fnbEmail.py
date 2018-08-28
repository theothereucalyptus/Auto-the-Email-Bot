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
	return now.strftime('%B') + ' ' + str(now.day) + ' ' + str(now.year)

def getMIME():
	text = '''
	Test table,
	{table}
	'''
	html = '''
	<html><body>
	<p>Test table, </p>
	{table}
	</body></html>
	'''
	with open('table.log') as tab:
		reader = csv.reader(tab)
		data = list(reader)

	test = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
	html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

	return MIMEMultipart("alternative", None, [MIMEText(text), MIMEText(html,'html')])
	
def main():
	usr = 'stacygaikovaia'
	passwd = getpass.getpass('Enter Password')

	serv = imaplib.IMAP4_SSL('imap.gmail.com')
	serv.login(usr, passwd)
	draft_dir = serv.select('[Gmail]/Drafts')

	new_message = getMIME()
	new_message['Subject'] = 'Food Not Bombs Sign Up Reminder (' + getdate() + ')'
	new_message['To'] = 'fnb@lists.wpirg.org'
	new_message['From'] = 'stacygaikovaia@gmail.com'

	serv.append('[Gmail]/Drafts', '',imaplib.Time2Internaldate(time.time()), str(new_message))

#	for emailid in items:
#		resp, data = serv.fetch(emailid, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
#		email_body = data[0][1] # getting the mail content
#		print email_body
#		mail = email.message_from_string(email_body) # parsing the mail content to get a mail object


if __name__ == '__main__':
	print getdate()
	res = main()
