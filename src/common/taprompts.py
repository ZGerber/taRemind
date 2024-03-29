#!/usr/bin/env python3
from typing import List, Dict, Tuple, Union

import inquirer
from rich import print

from common import get_weekdays
from databases import ContactQuery, ContactDatabase, MeetingQuery, MeetingDatabase

""" 
A collection of prompts from the Inquirer library. Used to collect information from the user.

TO DO: This module is disorganized. This can surely be done with less code.
"""


def add_contact() -> Tuple:
    questions = [ask_text("first_name",
                          message="Enter the FIRST name of the new contact"),
                 ask_text("last_name",
                          message="Enter the LAST name of the new contact"),
                 ask_text("email_address",
                          message="Enter the EMAIL ADDRESS of the new contact")]
    answers = inquirer.prompt(questions)
    return answers['first_name'], answers['last_name'], answers['email_address']


def delete_contact(names: List[str]) -> Dict:
    who = ask_list("name", "Which contact would you like to delete? (Choose one)", names)
    return inquirer.prompt(who)


def edit_contact(names: List[str], attributes: List[str]):
    who = ask_list("name", "Which contact would you like to edit? (Choose one)", names)
    what = ask_list("attribute", "What would you like to change? (Choose one)", attributes)
    return inquirer.prompt(who), inquirer.prompt(what)


def add_meeting():
    questions = [ask_text("meeting_name",
                          message="Enter the NAME of the new meeting"),
                 ask_list("meeting_day",
                          message="On which day of the week will the meeting occur?",
                          choices=get_weekdays())[0],
                 ask_text("meeting_time",
                          message="Enter the TIME at which the meeting will be held [HH:MM (24-hour clock)]"),
                 ask_text("zoom_link",
                          message="Enter the ZOOM LINK at which the meeting will be held (default=None)"),
                 ask_text("zoom_id",
                          message="Enter the ZOOM ID for the meeting (default=None)"),
                 ask_text("passcode",
                          message="Enter the ZOOM PASSCODE for the meeting (default=None)")]
    answers = inquirer.prompt(questions)
    return answers["meeting_name"], answers["meeting_day"], answers["meeting_time"], \
        answers["zoom_link"], answers["zoom_id"], answers["passcode"]


def delete_meeting(meetings: List[str]):
    which = ask_list("name", "Which meeting would you like to edit? (Choose one)", meetings)
    return inquirer.prompt(which)


def edit_meeting(meetings: List[str], attributes: List[str]):
    which = ask_list("name", "Which meeting would you like to edit? (Choose one)", meetings)
    what = ask_list("attribute", "What would you like to change? (Choose one)", attributes)
    return inquirer.prompt(which), inquirer.prompt(what)


def assign(names: List[str], meetings: List[str]):
    who = ask_list("name", "Choose a contact", names)
    person = inquirer.prompt(who)
    which = ask_checkbox("name", f"Which meeting(s) would you like to assign {person['name']} to? "
                                 f"(Use SPACE to select and ENTER to proceed)", meetings)
    meeting = inquirer.prompt(which)
    return person, meeting


def release(names: List[str], meetings: List[str]):
    who = ask_list("name", "Choose a contact", names)
    person = inquirer.prompt(who)
    which = ask_checkbox("name", f"Which meeting(s) would you like to release {person['name']} from? "
                                 f"(Use SPACE to select and ENTER to proceed)", meetings)
    meeting = inquirer.prompt(which)
    return person, meeting


def show_participants_by_meeting(meetings: List[str]):
    which = ask_checkbox('name', f"For which meeting(s) would you like view taParticipants? "
                                 f"(Use SPACE to select and ENTER to proceed)", meetings)
    return inquirer.prompt(which)


def show_meeting_by_participant(names: List[str]):
    who = ask_list('name', f"Choose a contact to see which meetings they participate in", names)
    return inquirer.prompt(who)


def choose_participation_view():
    which = ask_list('name', f"Choose an option", ["View all participants in a meeting",
                                                   "View all meetings for a participant"])
    return inquirer.prompt(which)


def create_reminder(meetings: Union[str, List[str]]):
    if isinstance(meetings, str):
        meeting_name = meetings
    else:
        meeting = inquirer.prompt(ask_list('name', "Which meeting would you like to set up a reminder for?", meetings))
        meeting_name = meeting['name']
    meeting_time = MeetingDatabase.get(MeetingQuery.meeting_name == meeting_name)['meeting_time']
    meeting_day = MeetingDatabase.get(MeetingQuery.meeting_name == meeting_name)['meeting_day']
    questions = [ask_list('day', f"The {meeting_name} occurs on {meeting_day} at {meeting_time}. "
                                 f"On what day would you like the reminder to be sent?",
                          get_weekdays())[0],
                 ask_text('time', f"Enter the time when the reminder email should be sent "
                                  f"[HH:MM (24-hour clock)]")]
    reminder = inquirer.prompt(questions)
    return meeting_name, meeting_day, meeting_time, reminder['day'], reminder['time']


def confirm(action: str, *args):
    """ Ask the user to confirm their input. The input parameter 'action' determines which request is sent.
    """
    if action == "add_contact":
        confirm_add = inquirer.confirm(f"Does this look correct?\n"
                                       f"First Name: {args[0]}\n"
                                       f"Last Name: {args[1]}\n"
                                       f"Email Address: {args[2]}\n")
        if confirm_add:
            print(f"[green]SUCCESS![/green] Added {args[0]} {args[1]} to the contact database!")
        else:
            print(f"{args[0]} {args[1]} [red]has not been added to the contact database[/red] ")
        return confirm_add

    elif action == "delete_contact":
        first_name = ContactDatabase.get(ContactQuery.position == args[0])['first_name']
        last_name = ContactDatabase.get(ContactQuery.position == args[0])['last_name']
        confirm_delete = inquirer.confirm(f"Are you sure you want to remove {first_name} {last_name} "
                                          f"from the contact database?")
        if confirm_delete:
            print(
                f"[green]Success![/green] Removed {first_name} {last_name} from the contact database.")
        else:
            print(f"{first_name} {last_name} [red]has not been removed from the contact database.[/red]")
        return confirm_delete

    elif action == "create_reminder":
        return inquirer.confirm("Would you like to set up a reminder for this meeting?")


def ask_text(key: str, message: str) -> object:
    """ Ask the user to input some text.
    """
    return inquirer.Text(key, message=message)


def ask_list(key: str, message: str, choices: List[str]):
    """ Ask the user to select only one option from a list.
    """
    return [inquirer.List(key, message=message, choices=choices)]


def ask_checkbox(key: str, message: str, choices: List[str]):
    """ Ask the user to select at least one option from a list.
    """
    return [inquirer.Checkbox(key, message=message, choices=choices)]

