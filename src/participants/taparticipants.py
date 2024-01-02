#!/usr/bin/env python3

from rich import print

from common import taprompts as UserPrompt
from databases import ContactQuery, MeetingQuery, ContactDatabase, MeetingDatabase
import databases.tacontacts_class as taContacts
import databases.tameetings_class as taMeetings


def append_participation_list():
    """ Add a new entry to the "participation" list for EACH contact, rather than updating a particular contact.
    This happens when a new meeting is created. The value of the appended entry is False by default.
    """
    for result in taContacts.Contact().query():
        participation_list = result['participation']
        participation_list.append(False)
        ContactDatabase.update({'participation': participation_list}, ContactQuery.position == result['position'])
    print("[bold green]DONE![/bold green]")


def remove_entry(pos: int) -> None:
    """ When a meeting is deleted, the corresponding entry in the participation list must be deleted for each
    contact.
    """
    for result in taContacts.Contact().query():
        participation_list = result['participation']
        participation_list.pop(pos - 1)
        ContactDatabase.update({'participation': participation_list}, ContactQuery.position == result['position'])


def assign() -> None:
    """ Assigns a contact as a meeting participant.
    """
    person, meeting = UserPrompt.assign(taContacts.Contact().query('name'),
                                        taMeetings.Meeting().query('meeting_name'))
    iperson = taContacts.get_contact_position(person['name'])
    # Meetings are numbered starting from 1. List indices start from zero. Making sure to change the right meeting:
    imeeting = [taMeetings.get_meeting_position(name) - 1 for name in meeting['name']]
    participation = ContactDatabase.search((ContactQuery['position'] == iperson))[0]['participation']
    for m, i in enumerate(imeeting):
        if participation[i]:
            print(f"[red]Oops![/red] {person['name']}"
                  f"[red] is already a participant in:[/red] {meeting['name'][m]}")
        else:
            participation[i] = not participation[i]
            print(f"[green]SUCCESS![/green] {person['name']} "
                  f"[green]has been assigned to:[/green] {meeting['name'][m]}")
            ContactDatabase.update({'participation': participation}, ContactQuery.position == iperson)


def release() -> None:
    """ Un-assigns a contact as meeting participant. The participant list for 'contact_position' is obtained,
    then the value at the index corresponding to 'meeting_position' is checked. If True, change it.
    Otherwise, print an "OK" message. The program doesn't care if the user tries to remove what isn't there.
    """
    person, meeting = UserPrompt.release(taContacts.Contact().query('name'),
                                         taMeetings.Meeting().query('meeting_name'))
    iperson = taContacts.get_contact_position(person['name'])
    # Meetings are numbered starting from 1. List indices start from zero. Make sure to change the right meeting:
    imeeting = [taMeetings.get_meeting_position(name) - 1 for name in meeting['name']]
    participation = ContactDatabase.search((ContactQuery['position'] == iperson))[0]['participation']
    for m, i in enumerate(imeeting):
        if participation[i]:
            participation[i] = not participation[i]
            print(f"[green]SUCCESS![/green] {person['name']} "
                  f"[green]is no longer a participant in the[/green] {meeting['name'][m]}")
        else:
            print(f"[red]Oops![/red] {person['name']} "
                  f"[red]is not a participant in this meeting:[/red] {meeting['name'][m]}")
    ContactDatabase.update({'participation': participation}, ContactQuery.position == iperson)


def get_participants(meeting_position: int):
    """ Return the names and email addresses of meeting participants.
    """
    ind = meeting_position - 1
    participant_names = []
    participant_emails = []
    results = taContacts.Contact().query()
    for result in results:
        participation_list = result['participation']
        if participation_list[ind]:
            participant_names.append((result['first_name'], result['last_name']))
            participant_emails.append(result['email_address'])
    return participant_names, participant_emails


def display():
    """ Show all participants for a given meeting, or vice-versa.
    """
    task = UserPrompt.choose_participation_view()

    if task['name'] == "View all participants in a meeting":
        meeting = UserPrompt.show_participants_by_meeting(taMeetings.Meeting().query('meeting_name'))
        imeeting = [taMeetings.get_meeting_position(name) - 1 for name in meeting['name']]
        for m, i in enumerate(imeeting):
            print(f"[magenta]The following contacts are participants in the[/magenta] {meeting['name'][m]}:")
            participant_names, _ = get_participants(i + 1)
            for name in participant_names:
                print("\t" + name[0] + " " + name[1])

    elif task['name'] == "View all meetings for a participant":
        person = UserPrompt.show_meeting_by_participant(taContacts.Contact().query('name'))
        participation = ContactDatabase.get((ContactQuery.first_name == person['name'].split()[0]) &
                                            (ContactQuery.last_name == person['name'].split()[1]))['participation']
        print(f"{person['name']} [magenta]participates in the following meetings:[/magenta]")
        for i, value in enumerate(participation):
            if value:
                meeting_number = i + 1
                print(f"\t {MeetingDatabase.get(MeetingQuery.position == meeting_number)['meeting_name']}")
