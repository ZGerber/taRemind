#!/usr/bin/env python3

import math
import os
import sys
from email.message import EmailMessage
import ssl
import smtplib
from typing import List
from datetime import datetime, timedelta

SENDER = os.environ.get("TA_REMIND_EMAIL")
PASSWORD = os.environ.get("GMAIL_PASSWORD")


def get_day_of_week(meeting_day: str):
    """
    Some email reminders don't get sent on the day of the meeting. This function checks to see if meeting_day
    matches the current day of the week. If so, the email will say "today". If not, it will say either "tomorrow" or the
    scheduled day (if the meeting is more than 1 day away).
    """
    if meeting_day == datetime.now().strftime('%A'):
        weekday = "today"
    elif meeting_day == datetime.strftime(datetime.now() + timedelta(1), '%A'):
        weekday = "tomorrow"
    else:
        weekday = meeting_day
    return weekday


def send_email(meeting_name: str,
               meeting_time: str,
               weekday: str,
               zoom_link: str,
               zoom_id: str,
               participants: List[str],
               passcode: str = None) -> None:

    subject = f'Reminder: {meeting_name}'
    body = f"""
    Hi everyone,
            
    This is a reminder that the {meeting_name} is {weekday} at {meeting_time} MDT over Zoom.
            
    {zoom_link} 
        
    Meeting ID: {zoom_id}    
    Passcode: {passcode}
    """

    email = EmailMessage()
    email['From'] = SENDER
    email['To'] = participants
    email['Subject'] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(SENDER, PASSWORD)
        smtp.sendmail(SENDER, participants, email.as_string())

    print(f"{meeting_name} email sent: {datetime.now().year}/{datetime.now().month}/{datetime.now().day} at "
          f"{datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")
