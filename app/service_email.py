#!/usr/bin/env python3

####################################################################################
# project: DNAC-ComplianceMon
# module: service_email.py
# author: kebaldwi@cisco.com
# use case: Simple Check of XML audit files against configuration
# developers:
#            Gabi Zapodeanu, TME, Enterprise Networks, Cisco Systems
#            Keith Baldwin, TSA, EN Architectures, Cisco Systems
#            Bryn Pounds, PSA, WW Architectures, Cisco Systems
####################################################################################

# This section sends emails

#     ------------------------------- IMPORTS -------------------------------
import datetime
import time
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import ssl
from config import SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASS, NOTIFICATION_EMAIL, TIME_ZONE

#     ----------------------------- DEFINITIONS -----------------------------

# This function sends an email notification.
def system_notification(ATTACHMENT):
    # Get Date and Time
    DATE, TIME = date_time(TIME_ZONE)

    # Compose the email message
    msg = MIMEMultipart()
    msg['From'] = SMTP_EMAIL
    msg['To'] = NOTIFICATION_EMAIL
    msg['Subject'] = 'DNA Center Compliance Report - ' + DATE + '.' 
    
    body = 'This is the report produced at ' + DATE + ' and ' + TIME + '.'
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach the file
    with open(ATTACHMENT, 'rb') as f:
        attachment = MIMEApplication(f.read(), _subtype='pdf')
        attachment.add_header('Content-Disposition', 'attachment', filename=ATTACHMENT)
        msg.attach(attachment)

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_EMAIL, SMTP_PASS)
        server.sendmail(SMTP_EMAIL, NOTIFICATION_EMAIL, msg.as_string())
    return

def system_message(MESSAGE):
    # Get Date and Time
    DATE, TIME = date_time(TIME_ZONE)
    
    # This is the main function for testing purposes
    subject = 'DNA Center Compliance System Message - ' + DATE + '.'
    body = MESSAGE
    message = f'Subject: {subject}\n\n{body}'
    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_EMAIL, SMTP_PASS)
        server.sendmail(SMTP_EMAIL, NOTIFICATION_EMAIL, message)
    return

def date_time(TIME_ZONE):
    # Get the current date time in UTC timezone
    now_utc = datetime.datetime.now(pytz.UTC)
    # Convert to timezone
    if TIME_ZONE == '':
        time_zone = 'US/Eastern'
    else:
        time_zone = TIME_ZONE
    tz = pytz.timezone(time_zone)
    
    # Check if the timezone is currently observing daylight savings time
    is_dst = bool(tz.localize(datetime.datetime.now()).dst())
    
    # Convert to the specified timezone while accounting for daylight savings time
    if is_dst:
        now_tz = datetime.datetime.now(tz)
    else:
        now_tz = tz.normalize(now_utc.astimezone(tz))
    
    # Format the date and time string
    date_str = now_tz.strftime('%m/%d/%Y')
    time_str = now_tz.strftime('%H:%M:%S')
    
    if is_dst:
        time_str += ' (DST)'
    return date_str, time_str

#     ----------------------------- MAIN -----------------------------
"""
message = 'this is a keith test from the system'
system_message(message)
attachment_path = './PrimeComplianceDev/COMPLIANCE_REPORT.pdf'
system_notification(attachment_path)
"""