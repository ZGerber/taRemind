#!/usr/bin/env python3

import common.taprompts as UserPrompt
import databases.tadatabases_class as taDatabases
import databases.tameetings_class as taMeetings
from common import check_dt
from databases import ReminderDatabase
from dataclasses import dataclass, field
from typing import List


@dataclass
class Remind(taDatabases.Database):
    reminder_attributes: List = field(default_factory=lambda: ["Meeting Name",
                                                               "Meeting Day",
                                                               "Meeting Time",
                                                               "Meeting Number",
                                                               "Reminder Day",
                                                               "Reminder Time"])

    def query(self, attribute="all"):
        if attribute == "all":
            return ReminderDatabase.all()
        else:
            return [result[attribute] for result in ReminderDatabase.all()]

    def display(self):
        """ Display all reminders in the database """
        col_width = max(len(str(word)) for result in self.query() for word in result.values()) + 2
        print("".join(word.ljust(col_width) for word in self.reminder_attributes))
        print("-"*col_width*len(self.reminder_attributes))
        for result in self.query():
            print("".join(str(word).ljust(col_width) for word in result.values()))
        return

    def add(self, new_meeting=False, name=None):
        """ Add a reminder to the database """
        if new_meeting:
            arg = name
        else:
            arg = taMeetings.Meeting().query("meeting_name")
        meeting_name, meeting_day, meeting_time, reminder_day, reminder_time = \
            UserPrompt.create_reminder(arg)
        check_dt(meeting_time)
        meeting_position = taMeetings.get_meeting_position(meeting_name)
        reminder = {
            "meeting_name": meeting_name,
            "meeting_day": meeting_day,
            "meeting_time": meeting_time,
            "meeting_position": meeting_position,
            "reminder_day": reminder_day,
            "reminder_time": reminder_time
        }
        ReminderDatabase.insert(reminder)
        return

    def delete(self):
        return

    def edit(self):

        return
