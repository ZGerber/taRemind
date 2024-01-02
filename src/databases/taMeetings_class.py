#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import List, Union

from rich import print
from rich.prompt import Prompt as p
from rich.table import Table

from common import get_weekdays
from databases import MeetingQuery, MeetingDatabase, ReminderDatabase, ReminderQuery, console
import databases.taDatabases_class as taDatabase
import databases.taReminder_class as taReminders
import taParticipants.taParticipants_class as taParticipants
import common.ta_prompts as UserPrompt


@dataclass
class Meeting(taDatabase.Database):
    meeting_attributes: List = field(default_factory=lambda: ["Meeting Name",
                                                              "Meeting Day",
                                                              "Meeting Time",
                                                              "Zoom Link",
                                                              "Zoom ID",
                                                              "Passcode"])

    def query(self, attribute="all"):
        """ Query the entire database.
        """
        if attribute == "all":
            return MeetingDatabase.all()
        else:
            return [result[attribute] for result in MeetingDatabase.all()]

    def display(self):
        """ Display a table of all meetings.
        """
        results = self.query()
        if not results:
            print("[red]No meetings found![/red]")
        table = configure_table()
        fill_table(table, results)
        console.print(table)

    def add(self):
        """ Add a new meeting to the database
        """

        meeting_name, meeting_day, meeting_time, zoom_link, zoom_id, passcode = UserPrompt.add_meeting()
        position = len(MeetingDatabase) + 1
        new_meeting = {
            'meeting_name': meeting_name,
            'meeting_day': meeting_day,
            'meeting_time': meeting_time,
            'zoom_link': zoom_link,
            'zoom_id': zoom_id,
            'passcode': passcode,
            'position': position
        }
        # Participant().append_participation_list()
        taParticipants.Participant.append_participation_list()
        MeetingDatabase.insert(new_meeting)
        reminder = UserPrompt.confirm("create_reminder")
        if reminder:
            taReminders.Remind().add(new_meeting=True, name=meeting_name)
        return

    def delete(self):
        """ Remove a meeting from the database
        """
        meeting = UserPrompt.delete_meeting(self.query("meeting_name"))
        if not meeting:
            self.display()
        else:
            pos = get_meeting_position(meeting['name'])
            MeetingDatabase.remove(MeetingQuery.position == pos)
            ReminderDatabase.remove(ReminderQuery.meeting_position == pos)  # Remove corresponding reminder
            reset_positions(pos)
            taParticipants.Participant().remove_entry(pos)
            print(f"[magenta]Removed meeting:[/magenta] {meeting['name']}")

    def edit(self):
        """ Edit a meeting.
        """
        meeting, attribute = UserPrompt.edit_meeting(self.query("meeting_name"), self.meeting_attributes)
        if not meeting:
            self.display()
        else:
            pos = get_meeting_position(meeting['name'])
            if attribute['attribute'] == "Meeting Name":
                MeetingDatabase.update({'meeting_name': p.ask("Enter the new Meeting Name")},
                                       MeetingQuery.position == pos)
            elif attribute['attribute'] == "Meeting Day":
                MeetingDatabase.update({'meeting_day': p.ask("Enter the new Meeting Day", choices=get_weekdays())},
                                       MeetingQuery.position == pos)
            elif attribute['attribute'] == "Meeting Time":
                MeetingDatabase.update({'meeting_time': p.ask("Enter the new Meeting Time")},
                                       MeetingQuery.position == pos)
            elif attribute['attribute'] == "Zoom Link":
                MeetingDatabase.update({'zoom_link': p.ask("Enter the new Zoom Link")},
                                       MeetingQuery.position == pos)
            elif attribute['attribute'] == "Zoom ID":
                MeetingDatabase.update({'zoom_id': p.ask("Enter the new Zoom ID")},
                                       MeetingQuery.position == pos)
            elif attribute['attribute'] == "Passcode":
                MeetingDatabase.update({'passcode': p.ask("Enter the new Passcode")},
                                       MeetingQuery.position == pos)
        return


def change_position(old_position: int, new_position: int) -> None:
    """ Changes position of meeting in the database.
    """
    MeetingDatabase.update({'position': new_position},
                           MeetingQuery.position == old_position)


def configure_table():
    table = Table(show_header=True, show_lines=True)
    table.add_column("Position", width=8, justify="center")
    table.add_column("Meeting Name", min_width=15, justify="center")
    table.add_column("Meeting Day", width=15, justify="center")
    table.add_column("Meeting Time", width=15, justify="center")
    table.add_column("Zoom Link", min_width=20, justify="center")
    table.add_column("Zoom Meeting ID", min_width=20, justify="center")
    table.add_column("Passcode", width=12, justify="center")
    return table


def fill_table(table, results):
    for meeting in results:
        table.add_row(f"[cyan]{meeting['position']}[/cyan]",
                      f"{meeting['meeting_name']}",
                      f"{meeting['meeting_day']}",
                      f"{meeting['meeting_time']}",
                      f"{meeting['zoom_link']}",
                      f"{meeting['zoom_id']}",
                      f"{meeting['passcode']}")


def get_meeting_position(entry: Union[str, int]) -> int:
    """ Gets a single entry from the meeting database. Returns the position number of that entry.
    Can accept either MEETING NAME or POSITION.
    """
    if entry.isdigit():
        position = entry
    else:
        name_string = ' '
        for i in entry.split():
            name_string = name_string + " " + i
        position = MeetingDatabase.get(MeetingQuery.meeting_name == name_string.strip())['position']
    return int(position)


def reset_positions(pos):
    """ After deleting a meeting, the positions of the remaining meetings need to be reset to keep them contiguous.
    """
    for i in range(pos + 1, len(Meeting().query()) + 2):
        change_position(i, i - 1)

