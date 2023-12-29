#!/usr/bin/env python3
import typer
from databases.contact import Contact
from databases.meeting import Meeting
from participants.participant import Participant
# from mail.

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


@app.command("show")
def show(database: str) -> None:
    """ Display all contacts, meetings, or participants in a given meeting.
    """
    if database == "contacts" or database == "contact":
        Contact().display()

    elif database == "meetings" or database == "meeting":
        Meeting().display()

    elif database == "participants" or database == "participant":
        Participant().display()


@app.command("add")
def add(database: str) -> None:
    """ Add a contact or meeting to the database.
    """
    if database == "contacts" or database == "contact":
        Contact().add()

    elif database == "meetings" or database == "meeting":
        Meeting().add()


@app.command("edit")
def edit(database: str) -> None:
    """ Edit an existing contact or meeting.
    """
    if database == "contacts" or database == "contact":
        Contact().edit()

    elif database == "meetings" or database == "meeting":
        Meeting().edit()


@app.command("delete")
def delete(database: str) -> None:
    """ Delete a contact or meeting from the database.
    """
    if database == "contacts" or database == "contact":
        Contact().delete()

    elif database == "meetings" or database == "meeting":
        Meeting().delete()


@app.command("assign")
def assign() -> None:
    """ Assign a contact to a meeting. Contacts assigned to a meeting are "participants".
    """
    Participant().assign()


@app.command("release")
def release() -> None:
    """ Remove a participant from a meeting.
    """
    Participant().release()


@app.command("send")
def send() -> None:
    """ Send an email reminder to meeting participants on a recurring basis.
    """
    Email().send()
    mtgs = meetings.read()
    meeting_ind = meeting_position - 1
    meeting_name = mtgs[meeting_ind].meeting_name
    meeting_day = mtgs[meeting_ind].meeting_day
    meeting_time = mtgs[meeting_ind].meeting_time
    zoom_link = mtgs[meeting_ind].zoom_link
    zoom_id = mtgs[meeting_ind].zoom_id
    passcode = mtgs[meeting_ind].passcode
    _, participant_emails = meetings.read_participants(meeting_position)

    weekday = send_mail.get_day_of_week(meeting_day)
    send_mail.send_email(meeting_name, meeting_time, weekday, zoom_link, zoom_id, participant_emails, passcode)


if __name__ == "__main__":
    app()
