#!/usr/bin/env python3
from typing import List, Any
from rich import print
import inquirer
from databases import ContactQuery, ContactDatabase
import calendar

""" 
A collection of prompts from the Inquirer library. 
Used to collect and/or confirm information from the user.
"""


def prompt(action: str) -> Any:
    """ Request input from the user, based upon parameter 'action'. Return the requested information.
    Questions come in three varieties:
        1) Using inquirer.Text() - The user types their response
        2) Using inquirer.List() - The user can select a single option from a list
        3) Using inquirer.Checkbox() - The user can select multiple options from a list.
    Questions are 'asked' by invoking the ask() and ask_multi() functions.
    """
    from databases.contact import Contact
    from databases.meeting import Meeting
    if action == "add_contact":
        questions = [ask("first_name",
                         message="Enter the FIRST name of the new contact")[0],
                     ask("last_name",
                         message="Enter the LAST name of the new contact")[0],
                     ask("email_address",
                         message="Enter the EMAIL ADDRESS of the new contact")[0]]
        answers = inquirer.prompt(questions)
        return answers['first_name'], answers['last_name'], answers['email_address']

    elif action == "delete_contact":
        who = ask("name", "Which contact would you like to delete? (Choose one)", Contact().get_names())
        return inquirer.prompt(who)

    elif action == "edit_contact":
        who = ask("name", "Which contact would you like to edit? (Choose one)", Contact().get_names())
        what = ask("attribute", "What would you like to change? (Choose one)", Contact().contact_attributes)
        return inquirer.prompt(who), inquirer.prompt(what)

    elif action == "add_meeting":
        questions = [ask("meeting_name",
                         message="Enter the NAME of the new meeting")[0],
                     ask_multi("meeting_day",
                               message="On which day(s) of the week will the meeting occur? "
                                       "(Use SPACE to select/deselect and ENTER to proceed)",
                               choices=list(calendar.day_name))[0],
                     ask("meeting_time",
                         message="Enter the TIME at which the meeting will be held [HH:MM (24-hour clock)]")[0],
                     ask("zoom_link",
                         message="Enter the ZOOM LINK at which the meeting will be held "
                                 "(This should be a recurring meeting)")[0],
                     ask("zoom_id",
                         message="Enter the ZOOM ID for the meeting")[0],
                     ask("passcode",
                         message="Enter the ZOOM PASSCODE for the meeting")[0]]

        answers = inquirer.prompt(questions)
        return answers["meeting_name"], answers["meeting_day"], answers["meeting_time"], \
            answers["zoom_link"], answers["zoom_id"], answers["passcode"]

    elif action == "delete_meeting":
        which = ask("name", "Which meeting would you like to edit? (Choose one)", Meeting().get_names())
        return inquirer.prompt(which)

    elif action == "edit_meeting":
        which = ask("name", "Which meeting would you like to edit? (Choose one)", Meeting().get_names())
        what = ask("attribute", "What would you like to change? (Choose one)", Meeting().meeting_attributes)
        return inquirer.prompt(which), inquirer.prompt(what)

    elif action == "assign":
        who = ask("name", "Choose a contact", Contact().get_names())
        person = inquirer.prompt(who)
        which = ask_multi("name", f"Which meeting(s) would you like to assign {person['name']} to? "
                                  f"(Use SPACE to select and ENTER to proceed)",
                          Meeting().get_names())

        meeting = inquirer.prompt(which)
        return person, meeting

    elif action == "release":
        who = ask("name", "Choose a contact", Contact().get_names())
        person = inquirer.prompt(who)
        which = ask_multi("name", f"Which meeting(s) would you like to release {person['name']} from? "
                                  f"(Use SPACE to select and ENTER to proceed)",
                          Meeting().get_names())
        meeting = inquirer.prompt(which)
        return person, meeting

    elif action == "show_participants":
        which = ask_multi('name', f"For which meeting(s) would you like view participants? "
                                  f"(Use SPACE to select and ENTER to proceed)",
                          Meeting().get_names())
        return inquirer.prompt(which)

    elif action == "show_opposite":
        who = ask('name', f"Choose a contact to see which meetings they participate in",
                  Contact().get_names())
        return inquirer.prompt(who)

    elif action == "participation_view":
        which = ask('name', f"Choose an option", ["View all participants in a meeting",
                                                  "View all meetings for a participant"])
        return inquirer.prompt(which)


def confirm(action: str, *args) -> None:
    """
    Ask the user to confirm their input. The input parameter 'action' determines which request is sent.
    """
    if action == "add_contact":
        confirm_add = [inquirer.Confirm(action,
                                        message=f"Does this look correct?\n"
                                                f"First Name: {args[0]}\n"
                                                f"Last Name: {args[1]}\n"
                                                f"Email Address: {args[2]}\n")]
        if inquirer.prompt(confirm_add)[f'{action}']:
            print(f"[green]SUCCESS![/green] Added {args[0]} {args[1]} to the contact database!")
        else:
            print(f"{args[0]} {args[1]} [red]has not been added to the contact database[/red] ")

    elif action == "delete_contact":
        first_name = ContactDatabase.get(ContactQuery.position == args[0])['first_name']
        last_name = ContactDatabase.get(ContactQuery.position == args[0])['last_name']
        confirm_delete = [inquirer.Confirm(action,
                                           message=f"Are you sure you want to remove {first_name} {last_name} "
                                                   f"from the contact database?")]
        if inquirer.prompt(confirm_delete)[f'{action}']:
            print(
                f"[green]Success![/green] Removed [magenta]{first_name} {last_name}[/magenta] from the contact database.")
        else:
            print(f"{first_name} {last_name} [red]has not been removed from the contact database.[/red]")


def ask(key: str, message: str, choices: List[str] = None) -> object:
    """ Ask the user to select a single option from a list.
    """
    if choices:
        return [inquirer.List(key, message=message, choices=choices)]
    else:
        return [inquirer.Text(key, message=message)]


def ask_multi(key: str, message: str, choices: List[str]) -> object:
    """ Ask the user to select at least one option from a list.
    """
    return [inquirer.Checkbox(key, message=message, choices=choices)]
