#!/usr/bin/env python3

from apscheduler.schedulers.background import BackgroundScheduler, BlockingScheduler


def create_job(func, meeting_position):
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(func, trigger='interval', seconds=3, args=[meeting_position])
    scheduler.start(job)
    return scheduler, job

    # return scheduler.add_job(create_job, trigger='cron', second="*/10")


# scheduler = BackgroundScheduler()

# scheduler.add_job(create_job, trigger='cron', second="*/10")


