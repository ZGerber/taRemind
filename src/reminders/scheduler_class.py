#!/usr/bin/env python3

from dataclasses import dataclass
from reminders.reminder_class import send_email
from schedule import every, repeat, run_pending


@repeat(every().sunday.at("09:00"))
def job():
    send_email(8)


@dataclass
class Scheduler:
    meeting_name: str
    meeting_day: str
    meeting_time: str
    reminder_day: str
    reminder_time: str


while True:
    run_pending()
