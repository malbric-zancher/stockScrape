#!/usr/bin/env python

import requests, bs4, sys, smtplib, datetime
from email.mime.text import MIMEText

# email function
def sendEmail(emailText):
	emailMsg = MIMEText(emailText)
	emailMsg['Subject'] = '%s %s price breakeven information' % (datetime.date.today(), sys.argv[1])
	emailMsg['From'] = 'root@blecharz.eu'
	emailMsg['To'] = 'marcinblecharz@gmail.com'
	
	s = smtplib.SMTP('blecharz.eu', 25)
	s.sendmail('root@blecharz.eu', ['marcinblecharz@gmail.com'], emailMsg.as_string())
	s.quit()

# usage information and basic arguments check	
if len(sys.argv) < 3:
	print('usage: script [ticker] [target_price]\nscript opl 6.00')
	sys.exit(0)

url = 'https://stooq.pl/q/g/?s=' + sys.argv[1]

# basic check for float in 2nd argument
try:
	targetPrice = float(sys.argv[2])

except Exception as exc:
	print('Gimme a float/number, got Exception: %s') % exc
	sys.exit(1)

pageData = requests.get(url)

# catch errors other than HTTP 200
try:
	pageData.raise_for_status()

except Exception as exc:
	sendEmail('Errored out: %s') % exc
	sys.exit(1)

beautifulData = bs4.BeautifulSoup(pageData.text, "html.parser")

# catch HTTP 200 but nonexistent tickers nonetheless
try:
	rawTag = beautifulData.select('tr #f13 > td > b')[0]

except IndexError as ind:
	sendEmail('Probably wrong ticker: %s') % ind
	sys.exit(1)

cleanPrice = str(rawTag).strip('<b> </')
floatPrice = float(cleanPrice)

# basic price compare
if floatPrice > targetPrice:
	priceText = '''Current price: %s
Target price: %s
Researched url: %s
''' % (floatPrice, targetPrice, url)
	sendEmail(priceText)

else:
	pass
