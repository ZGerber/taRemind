#!/usr/bin python3

import calendar
from typing import List


def get_weekdays() -> List[str]:
    """ Return a list of the weekday names"""
    return list(calendar.day_name)

