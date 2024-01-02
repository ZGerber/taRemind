#!/usr/bin python3

import calendar
from datetime import datetime


def get_weekdays():
    """ Return a list of the weekday names"""
    return list(calendar.day_name)


def time2dt(input_time: str, fmt):
    """ Convert a string in the format HHMM or HH:MM or HH to datetime object"""
    return datetime.strptime(input_time, fmt)


def check_dt(input_time):
    """ Check whether input time is in an acceptable format """
    for fmt in ['%H:%M']:
        try:
            return time2dt(input_time, fmt)
        except ValueError:
            pass
    raise ValueError(f"ERROR! Invalid format. Should be HH:MM (24-hour clock) '{input_time}'")


def abbreviate_weekday(day: str):
    return day[0:3].lower()


def get_hour(dt):
    t = time2dt(dt, "%H:%M")
    return t.hour


def get_minute(dt):
    t = time2dt(dt, "%H:%M")
    return t.minute
