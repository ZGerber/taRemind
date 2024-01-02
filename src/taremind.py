#!/usr/bin/env python3
import typer

import databases.tareminder_class as taReminders
import databases.tacontacts_class as taContacts
import databases.tameetings_class as taMeetings
import reminder_emails.tascheduler as taScheduler
import participants.taparticipants as taParticipants

app = typer.Typer(add_completion=False, no_args_is_help=True,
                  context_settings=dict(help_option_names=['-h', '--help']),
                  help="This program is used to manage contacts and meetings, and to send automated email reminder_emails "
                       "to meeting participants. Contacts are stored in a database called contact-book, which is "
                       "in the JSON format. Contacts can be added, removed, or edited, and the contact book can be "
                       "printed to the console. Similarly, meetings are stored in a database called meeting-book, "
                       "also in the JSON format. Meetings can be created, deleted, or edited, and the meeting book can "
                       "be printed to the console. Contacts can be assigned to (or released from) meetings. "
                       "If assigned, contacts become 'participants'. Participants will receive email reminders "
                       "regarding their upcoming meetings.")


@app.command("show")
def show(database: str) -> None:
    """ Display all contacts, meetings, participants, or reminders for a given meeting.
    """
    if database == "contacts" or database == "contact" or database == "c":
        taContacts.Contact().display()

    elif database == "meetings" or database == "meeting" or database == "m":
        taMeetings.Meeting().display()

    elif database == "participants" or database == "participant" or database == "p":
        taParticipants.display()

    elif database == "reminders" or database == "reminder" or database == "r":
        taReminders.Remind().display()


@app.command("add")
def add(database: str) -> None:
    """ Add a contact or meeting to the database.
    """
    if database == "contacts" or database == "contact":
        taContacts.Contact().add()

    elif database == "meetings" or database == "meeting":
        taMeetings.Meeting().add()

    elif database == "reminders" or database == "reminder":
        taReminders.Remind().add()


@app.command("edit")
def edit(database: str) -> None:
    """ Edit an existing contact or meeting.
    """
    if database == "contacts" or database == "contact":
        taContacts.Contact().edit()

    elif database == "meetings" or database == "meeting":
        taMeetings.Meeting().edit()

    elif database == "reminders" or database == "reminder":
        taReminders.Remind().edit()


@app.command("delete")
def delete(database: str) -> None:
    """ Delete a contact or meeting from the database.
    """
    if database == "contacts" or database == "contact":
        taContacts.Contact().delete()

    elif database == "meetings" or database == "meeting":
        taMeetings.Meeting().delete()

    elif database == "reminders" or database == "reminder":
        taReminders.Remind().delete()


@app.command("assign")
def assign() -> None:
    """ Assign a contact to a meeting. Contacts assigned to a meeting are "participants".
    """
    taParticipants.assign()


@app.command("release")
def release() -> None:
    """ Remove a participant from a meeting.
    """
    taParticipants.release()


@app.command("start")
def start() -> None:
    """ Start the email daemon in the background. This will cause all reminders in the database to be
    sent at their scheduled times. This should be started whenever the host computer is rebooted. """
    taScheduler.start_daemon()


if __name__ == "__main__":
    app()
