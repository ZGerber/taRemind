#!/usr/bin/env python3
import typer

import databases.tacontacts_class as taContacts
import databases.tameetings_class as taMeetings
import databases.tareminder_class as taReminders
import participants.taparticipants as taParticipants
import reminder_emails.tascheduler as taScheduler

app = typer.Typer(add_completion=False, no_args_is_help=True,
                  context_settings=dict(help_option_names=['-h', '--help']),
                  help="This program is used to manage contacts and meetings, and to send automated email reminders "
                       "to meeting participants. Contacts are stored in a database called contact-book, which is "
                       "in the JSON format. Contacts can be added, removed, or edited, and the contact book can be "
                       "printed to the console. Similarly, meetings are stored in a database called meeting-book, "
                       "also in the JSON format. Meetings can be created, deleted, or edited, and the meeting book can "
                       "be printed to the console. Contacts can be assigned to (or released from) meetings. "
                       "If assigned, contacts become 'participants'. Participants will receive email reminders "
                       "regarding their upcoming meetings.")

contact_options = ["contacts", "contact", "c", "people"]
meeting_options = ["meetings", "meeting", "m", "meet"]
participant_options = ["participants", "participant", "p"]
reminder_options = ["reminders", "reminder", "remind", "r"]


@app.command("show")
def show(database: str) -> None:
    """ Display all contacts, meetings, participants, or reminders for a given meeting.
    """
    if database in contact_options:
        taContacts.Contact().display()

    elif database in meeting_options:
        taMeetings.Meeting().display()

    elif database in participant_options:
        taParticipants.display()

    elif database == reminder_options:
        taReminders.Remind().display()


@app.command("add")
def add(database: str) -> None:
    """ Add a contact, meeting or reminder to the database. """
    if database in contact_options:
        taContacts.Contact().add()

    elif database in meeting_options:
        taMeetings.Meeting().add()

    elif database in reminder_options:
        taReminders.Remind().add()


@app.command("edit")
def edit(database: str) -> None:
    """ Edit an existing contact or meeting.
    """
    if database in contact_options:
        taContacts.Contact().edit()

    elif database in meeting_options:
        taMeetings.Meeting().edit()

    elif database in reminder_options:
        taReminders.Remind().edit()


@app.command("delete")
def delete(database: str) -> None:
    """ Delete a contact or meeting from the database.
    """
    if database in contact_options:
        taContacts.Contact().delete()

    elif database in meeting_options:
        taMeetings.Meeting().delete()

    elif database in reminder_options:
        taReminders.Remind().delete()


@app.command("assign")
def assign() -> None:
    """ Assign a contact to a meeting. Contacts assigned to a meeting are "participants".
    """
    taParticipants.assign()


@app.command("release")
def release() -> None:
    """ Remove a participant from a meeting. """
    taParticipants.release()


@app.command("start")
def start() -> None:
    """ Start the email daemon in the background. This will cause all reminders in the database to be
    sent at their scheduled times. This should be started whenever the host computer is rebooted. """
    taScheduler.run_scheduler()


if __name__ == "__main__":
    app()
