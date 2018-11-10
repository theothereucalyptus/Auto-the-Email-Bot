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

def calctimedelta(now):
    weekday = now.weekday()
    if (weekday == 6):  #sunday
		return 6
    else:
		return (5 - weekday) 

def getdate():
	now = datetime.date.today()
	date2 = now + datetime.timedelta(days=calctimedelta(now))
	return date2.strftime('%B') + ' ' + str(date2.day) + ' ' + str(date2.year)

def parselog(filename):
	table = '' 
	with open(filename) as csvFile: 
		reader = csv.DictReader(csvFile, delimiter=',')    
		table = '<tr>{}</tr>'.format(''.join(['<td class="cell">{}</td>'.format(header) for header in reader.fieldnames])) 
		for row in reader:  
			table_row = '<tr>' 
			for fn in reader.fieldnames:            
				table_row += '<td class="cell">{}</td>'.format(row[fn]) 
			table_row += '</tr>' 
			table += table_row
	return table

def getMIME():
	table = parselog('table.log')
	
	text = '''
	Hello fine folks, \n
	It's time to sign up for Food Not Bombs once again :)\n Please sign up for the tasks that you're planning to do on the sign up sheet: https://docs.google.com/spreadsheets/d/1rOeV_fEl_1wLedUWv44LzcK3VeLCGiL-UmRRyu-8KIg/edit#gid=1078847430
	
	Here is a table of the usual tasks: 
	{table}
	
	Take care, 
	Auto the Email Robot \n
	PS: I am a robot writted by Stacy Gaikovaia. Please email stacygaikovaia@gmail.com if I am making mistakes or you have any suggestions for improvements
	'''

	html = '''
	<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>html title</title>
	<style type="text/css" media="screen">
	table{
	    background-color: white;
	    empty-cells:hide;
	    Border:5px solid black;
	 }
	 td.cell{
	    background-color: white;
            Border:2px solid black;
	 }
	</style></head>
	<html><body>
	<p>Hello fine folks, </p>
	<p>It's time to sign up for Food Not Bombs once again :)</p>
	<p>Please sign up for the tasks that you're planning to do <a href="https://docs.google.com/spreadsheets/d/1rOeV_fEl_1wLedUWv44LzcK3VeLCGiL-UmRRyu-8KIg/edit#gid=1078847430">on the sign-up sheet!</a></p><br>
	<p>Here is a table of the usual tasks:</p>
	<table style="border: black 5px;">
	%s
	</table>
	<p>Take care, <br>
	Auto the Email Robot<br><br>
	Blep Blop! I am a robot written by Stacy Gaikovaia. Please email stacygaikovaia@gmail.com if I am making mistakes or if you have any suggestions for improvements</p>
	</body></html> 
	''' % table
	with open('table.log') as tab:
		reader = csv.reader(tab)
		data = list(reader)

	text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"))
#	html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"))

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
	main()
