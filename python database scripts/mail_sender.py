# -*- coding: utf-8 -*-
# import smtplib
# fromaddr = 'rafanketaizvestaj@gmail.com'
# toaddrs  = 'ivandejkovic95@gmail.com'
# msg = "\r\n".join([
#   "From: user_me@gmail.com",
#   "To: user_you@gmail.com",
#   "Subject: Just a message",
#   "",
#   "It works"
#   ])
# username = 'rafanketaizvestaj@gmail.com'
# password = 'racunarski1'
# server = smtplib.SMTP('smtp.gmail.com:587')
# server.ehlo()
# server.starttls()
# server.login(username,password)
# server.sendmail(fromaddr, toaddrs, msg)
# server.quit()


################################################
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
import datetime
import codecs

smtpUser = 'rafanketaizvestaj@gmail.com'
smtpPass = 'racunarski1'

toAdd = 'ivandejkovic95@gmail.com'
fromAdd = smtpUser

today = datetime.date.today()

subject = 'attach proba'
header = 'To :' + toAdd + '\n' + 'From : ' + fromAdd + '\n' + 'Subject : ' + subject + '\n'
body = 'This is a data file on %s' % today.strftime('%Y %b %d')
attach = 'Data on %s.csv' % today.strftime('%Y-%m-%d')


def sendMail(to, subject, text, files=[]):
    assert type(to)==list
    assert type(files)==list

    msg = MIMEMultipart()
    msg['From'] = smtpUser
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach( MIMEText(text) )

    for file in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(file,"rb").read() )
        #part.set_payload(codecs.open(file, "rb", "utf-8").read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(file))
        msg.attach(part)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(smtpUser,smtpPass)
    server.sendmail(smtpUser, to, msg.as_string())

    print 'Done'

    server.quit()


#sendMail( ['ivandejkovic95@gmail.com'], subject, body, ['nastavnicki_izvestaji/random.txt'] )
