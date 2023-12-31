#!/usr/bin/env python3
import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage
from typing import List

import reminders
from common import user_prompts as UserPrompt
from databases import MeetingDatabase, MeetingQuery
from databases.meeting_class import Meeting
from participants.participant_class import Participant


def get_meeting_name(position: int) -> str:
    """ Accepts the position number of a meeting and returns its name.
    """
    return MeetingDatabase.get(MeetingQuery.position == position)['meeting_name']


def get_meeting_day(position: int) -> str:
    """ Accepts the position number of a meeting and returns the day on which it occurs.
    """
    return MeetingDatabase.get(MeetingQuery.position == position)['meeting_day']


def get_meeting_time(position: int) -> str:
    """ Accepts the position number of a meeting and returns the time at which it occurs.
    """
    return MeetingDatabase.get(MeetingQuery.position == position)['meeting_time']


def get_zoom_link(position: int) -> str:
    """ Accepts the position number of a meeting and returns its zoom link.
    """
    return MeetingDatabase.get(MeetingQuery.position == position)['zoom_link']


def get_zoom_id(position: int) -> str:
    """ Accepts the position number of a meeting and returns its zoom id.
    """
    return MeetingDatabase.get(MeetingQuery.position == position)['zoom_id']


def get_zoom_passcode(position: int) -> str:
    """ Accepts the position number of a meeting and returns its zoom passcode.
    """
    return MeetingDatabase.get(MeetingQuery.position == position)['passcode']


def get_day_of_week(meeting_day: str):
    """ Some email reminders don't get sent on the day of the meeting. This function checks to see if meeting_day
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


def recipients(position: int) -> List[str]:
    """ Accepts the position number of a meeting and returns a list of the recipients' email addresses.
    """
    _, email_addresses = Participant().get_participants(position)
    return email_addresses


def email_subject(position: int) -> str:
    """ Accepts the position number of a meeting and returns a string which serves as the email subject.
    """
    return f'Reminder: {get_meeting_name(position)}'


def email_body(position: int) -> str:
    """ Accepts the position number of a meeting and returns a string that serves as the body of the email.
    """
    return f"""
    Hi everyone,
            
    This is a reminder that the {get_meeting_name(position)} is {get_day_of_week(get_meeting_day(position))} at {get_meeting_time(position)} MDT over Zoom.

    {get_zoom_link(position)} 

    Meeting ID: {get_zoom_id(position)}    
    Passcode: {get_zoom_passcode(position)}
    """


def create_email(position: int):
    email = EmailMessage()
    email['From'] = reminders.EmailInfo.SENDER
    email['To'] = recipients(position)
    email['Subject'] = email_subject(position)
    email.set_content(email_body(position))
    return email.as_string()


def send_email(position: int):
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context()) as smtp:
        smtp.login(reminders.EmailInfo.SENDER, reminders.EmailInfo.PASSWORD)
        smtp.sendmail(reminders.EmailInfo.SENDER, recipients(position), create_email(position))
    print(f"{get_meeting_name(position)} email sent: {datetime.now().year}/{datetime.now().month}/{datetime.now().day} "
          f"at {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}")


def remind():
    meeting, meeting_day, meeting_time, reminder_day, reminder_time = UserPrompt.create_reminder(Meeting().get_names())
    meeting_position = Meeting().get_position(meeting['name'])
    reminders.r