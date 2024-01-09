#!/usr/bin/env python3

from apscheduler.schedulers.background import BlockingScheduler

import databases.tareminder_class as taReminders
import reminder_emails.taemails as taEmails
from common import abbreviate_weekday, get_hour, get_minute


def run_scheduler():
    scheduler = BlockingScheduler()
    for reminder in taReminders.Remind().query():
        scheduler.add_job(func=taEmails.send_email,
                          trigger='cron',
                          day_of_week=abbreviate_weekday(reminder['reminder_day']),
                          hour=get_hour(reminder['reminder_time']),
                          minute=get_minute(reminder['reminder_time']),
                          args=[reminder['meeting_position']])
    scheduler.start()



