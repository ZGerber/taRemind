#!/usr/bin/env python3

# from reminders.reminder_class import send_email
from apscheduler.schedulers.background import BackgroundScheduler


def create_job():
    print("GOT HERE")
    # return scheduler.add_job()
    # send_email(8)


scheduler = BackgroundScheduler()
scheduler.add_job(create_job, trigger='cron', second="*/5")

scheduler.start()
