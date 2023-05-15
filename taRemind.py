#!/usr/bin/env python

import typer
import datetime
from models.taRemind_models import Contact, Meeting
import util.contacts as c
import util.meetings as m
from mail import send_email
import os
from rich import print
from rich.console import Console
from rich.table import Table
from typing_extensions import Annotated
from typing import List

console = Console()

app = typer.Typer(add_completion=False, no_args_is_help=True,
                  help="This program is used to manage contacts and meetings for the Cosmic Ray Group, and to send"
                       " automated email reminders to meeting participants.\n\n"
                       "Contacts are stored in a database called contact-book, which is in the JSON format.\n"
                       "Contacts can be added, removed, or edited, and the contact book can be printed to the "
                       "console.\n\n"
                       "Similarly, meetings are stored in a database called meeting-book, also in the JSON format.\n"
                       "Meetings can be created, deleted, or edited, and the meeting book can be printed to the "
                       "console.\n\n"
                       "Contacts can be assigned to (or released from) meetings. If assigned, contacts become\n"
                       "'participants'. Participants will receive email reminders regarding their upcoming "
                       "meetings.\n\n")
contacts_app = typer.Typer()
meetings_app = typer.Typer()
app.add_typer(contacts_app, name="contacts", short_help="View or edit the contact book. "
                                                        "Use 'taRemind.py contacts --help' for more information")
app.add_typer(meetings_app, name="meetings", short_help="View or edit the meeting book. "
                                                        "Use 'taRemind.py meetings --help' for more information")


@contacts_app.command("add", short_help='Add a contact to contact book')
def add_contact(first_name: Annotated[str, typer.Argument(help="First name of the person you wish to add")],
                last_name: Annotated[str, typer.Argument(help="Last name of the person you wish to add")],
                email_address: Annotated[str, typer.Argument(help="Email address of the person you wish to add")]) -> None:
    """
    Add a contact to the contact book. Required arguments are first name, last name, and email address.
    """
    print(f"[magenta]Adding[/magenta] {first_name} {last_name}; {email_address} [magenta]to contact book[/magenta]")
    contact = Contact(first_name, last_name, email_address)
    c.create(contact)
    get_contacts()


@meetings_app.command("add", short_help='Add a meeting to meeting book')
def add_meeting(meeting_name: Annotated[str, typer.Argument(help="Name of the meeting")],
                meeting_day: Annotated[str, typer.Argument(help="Day of the week on which the meeting is held.")],
                meeting_time: Annotated[str, typer.Argument(help="Time at which the meeting is held (MDT).")],
                zoom_link: Annotated[str, typer.Argument(help="Zoom link for the meeting.")],
                passcode: Annotated[int, typer.Argument(help="Passcode for the Zoom meeting.")] = None) -> None:
    """
    Add a meeting to the meeting book. Required arguments are meeting name, meeting time, and Zoom link.
    Optional argument is passcode for zoom link.
    """
    print(f"[magenta]Creating[/magenta] {meeting_name} [magenta]meeting on[/magenta] {meeting_day}s "
          f"[magenta]at[/magenta] [white]{meeting_time} MDT[/white]")
    meeting = Meeting(meeting_name, meeting_day, meeting_time, zoom_link, passcode)
    m.create(meeting)
    get_meetings()


@contacts_app.command("show", short_help='Display all contacts in contact book')
def get_contacts() -> None:
    """
    Display all contacts in the contact book.
    """
    contacts = c.read()
    if not contacts:
        print("[red]No contacts found.[/red]")
    else:
        table = Table(show_header=True, show_lines=True, title="[bold cyan]THE BOOK OF COSMIC CONTACTS:[/bold cyan]")
        table.add_column("Position", width=8, justify="center")
        table.add_column("Name", min_width=20, justify="center")
        table.add_column("Email Address", min_width=20, justify="center")
        for idx, contact in enumerate(contacts, start=1):
            table.add_row(f"[cyan]{idx}[/cyan]",
                          f"[bold]{contact.first_name} {contact.last_name}[/bold]",
                          f"{contact.email_address}")
        console.print(table)


@meetings_app.command("show", short_help='Display all meetings')
def get_meetings() -> None:
    """
    Display all meetings in the meeting book.
    """
    meetings = m.read()
    if not meetings:
        print("[red]No meetings found.[/red]")
    else:
        table = Table(show_header=True, show_lines=True, title="[bold cyan]THE BOOK OF COSMIC MEETINGS:[/bold cyan]")
        table.add_column("Position", width=8, justify="center")
        table.add_column("Meeting Name", min_width=15, justify="center")
        table.add_column("Meeting Day", width=15, justify="center")
        table.add_column("Meeting Time", width=15, justify="center")
        table.add_column("Zoom Link", min_width=20, justify="center")
        table.add_column("Passcode", width=12, justify="center")
        for idx, meeting in enumerate(meetings, start=1):
            table.add_row(f"[cyan]{idx}[/cyan]",
                          f"{meeting.meeting_name}",
                          f" {meeting.meeting_day}",
                          f" {meeting.meeting_time}",
                          f"{meeting.zoom_link}",
                          f"{meeting.passcode}")
        console.print(table)


@contacts_app.command("edit", short_help='Edit a contact')
def edit_contact(position: int,
                 first_name: str = None,
                 last_name: str = None,
                 email_address: str = None) -> None:
    """
    Edit a contact. The required argument is the position number of the contact you wish to edit. \n
    (Position number can be found by running 'taRemind.py contacts show')
    """
    print(f"[magenta]Editing[/magenta] {position}")
    c.update(position, first_name, last_name, email_address)
    print("[bold green]DONE![/bold green]")
    get_contacts()


@meetings_app.command("edit", short_help='Edit a meeting')
def edit_meeting(position: int,
                 meeting_name: str = None,
                 meeting_day: str = None,
                 meeting_time: str = None,
                 zoom_link: str = None,
                 passcode: str = None) -> None:
    """
    Edit a meeting. The required argument is the position number of the meeting you wish to edit. \n
    (Position number can be found by running 'taRemind.py meetings show')
    """
    print(f"[magenta]Editing[/magenta] {position}")
    m.update(position, meeting_name, meeting_day, meeting_time, zoom_link, passcode)
    print("[bold green]DONE![/bold green]")
    get_meetings()


@contacts_app.command("remove", short_help='Remove a contact from contact book')
def remove_contact(position: int) -> None:
    """
    Remove a contact. The required argument is the position number of the contact you wish to remove. \n
    (Position number can be found by running 'taRemind.py contacts show')
    """
    print(f"[magenta]Removing[/magenta] {position}")
    c.delete(position)
    print("[bold green]DONE![/bold green]")
    get_contacts()


@meetings_app.command("remove", short_help='Remove a meeting from meeting book')
def remove_meeting(position: int) -> None:
    """
    Remove a meeting. The required argument is the position number of the meeting you wish to remove. \n
    (Position number can be found using 'taRemind.py meetings show')
    """
    print(f"[magenta]Removing[/magenta] {position}")
    m.delete(position)
    print("[bold green]DONE![/bold green]")
    get_meetings()


@meetings_app.command("participants", short_help="Display list of meeting participants")
def get_participants(position: int) -> None:
    """
    Get list of meeting participants.
    """
    participants, _ = m.read_participants(position)
    if not participants:
        print(f"[bold red]This meeting does not have any participants! It will be quite boring.[/bold red]")
    else:
        print(f"[underline][bold magenta]There are[/bold magenta] {len(participants)} "
              f"[bold magenta]participants in meeting[/bold magenta] {position}[/underline]:")
        for participant in participants:
            print(f"{participant[0]} {participant[1]}")


@meetings_app.command("assign", short_help="Assign contact to meeting as participant")
def assign_participant(contact_position: int,
                       meeting_position: int) -> None:
    """
    Assign a contact to a meeting. Contacts assigned to a meeting are "participants".
    """
    print(f"[magenta]Assigning contact[/magenta] {contact_position} [magenta]to meeting[/magenta] {meeting_position}")
    m.add_participant(contact_position, meeting_position)


@meetings_app.command("release", short_help="Remove participant from meeting")
def release_participant(contact_position: int, meeting_position: int) -> None:
    """
    Remove a participant from a meeting.
    """
    print(f"Removing {contact_position} from {meeting_position}")
    m.delete_participant(contact_position, meeting_position)


@app.command("send", short_help="Send an email reminder to meeting participants")
def send_email(meeting_position: int):
    meetings = m.read()
    meeting_ind = meeting_position - 1
    meeting_name = meetings[meeting_ind].meeting_name
    meeting_time = meetings[meeting_ind].meeting_time
    zoom_link = meetings[meeting_ind].zoom_link
    passcode = meetings[meeting_ind].passcode
    _, participant_emails = m.read_participants(meeting_position)
    new_sendmail.send_email(meeting_name, meeting_time, zoom_link, participant_emails, passcode)


if __name__ == "__main__":
    app()
