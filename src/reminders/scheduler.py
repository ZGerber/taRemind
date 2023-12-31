#!/usr/bin/env python3

from typing import Dict
import schedule
import time
from databases.meeting import Meeting
from common import user_prompts as UserPrompt
from reminders import reminder_email as Email



# def reminder_day():

# mtgs = meetings.read()
# meeting_ind = meeting_position - 1
# meeting_name = mtgs[meeting_ind].meeting_name
# meeting_day = mtgs[meeting_ind].meeting_day
# meeting_time = mtgs[meeting_ind].meeting_time
# zoom_link = mtgs[meeting_ind].zoom_link
# zoom_id = mtgs[meeting_ind].zoom_id
# passcode = mtgs[meeting_ind].passcode
# _, participant_emails = meetings.read_participants(meeting_position)
#
# weekday = send_mail.get_day_of_week(meeting_day)
# send_mail.send_email(meeting_name, meeting_time, weekday, zoom_link, zoom_id, participant_emails, passcode)