import math
import os
from email.message import EmailMessage
import ssl
import smtplib
from typing import List

SENDER = 'ta-remind@cosmic.utah.edu'
PASSWORD = os.environ.get("GMAIL_PASSWORD")


def send_email(meeting_name: str,
               meeting_time: str,
               zoom_link: str,
               participants: List[str],
               passcode: str = None) -> None:

    subject = f'Reminder: {meeting_name}'
    body = f"""
            Hello,
            
            This is a reminder that the {meeting_name} is today at {meeting_time} MDT over Zoom.
            
            {zoom_link}
            
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
