#!/usr/bin/env python3

from common import check_dt
import common.taprompts as UserPrompt
import databases.tadatabases_class as taDatabases
import databases.tameetings_class as taMeetings
from databases import ReminderDatabase, ReminderQuery


class Remind(taDatabases.Database):

    def query(self, attribute="all"):
        if attribute == "all":
            return ReminderDatabase.all()
        else:
            return [result[attribute] for result in ReminderDatabase.all()]

    def display(self):
        """ Temporary: Just print each entry (dictionary) in the database. """
        for result in self.query():
            print(result)
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
