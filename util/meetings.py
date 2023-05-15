#!/usr/bin/env python

from typing import List, Tuple, Any
from models.taRemind_models import Contact, Meeting
import util.contacts as c
from meetings import meeting_db, MeetingQuery
from contacts import contact_db, ContactQuery
from rich import print


def create(meeting: Meeting) -> None:
    """
    Insert new meeting into database.
    """
    meeting.position = len(meeting_db) + 1
    new_meeting = {
        'meeting_name': meeting.meeting_name,
        'meeting_day': meeting.meeting_day,
        'meeting_time': meeting.meeting_time,
        'zoom_link': meeting.zoom_link,
        'passcode': meeting.passcode,
        'position': meeting.position
    }
    c.update(None, None, None, None, participation=True)
    meeting_db.insert(new_meeting)
    print("[bold green]DONE![/bold green]")


def read() -> List[Meeting]:
    """
    Returns a list of all meetings in the database.
    """
    results = meeting_db.all()
    meetings = []
    for result in results:
        meeting = Meeting(result['meeting_name'],
                          result['meeting_day'],
                          result['meeting_time'],
                          result['zoom_link'],
                          result['passcode'],
                          result['position'])
        meetings.append(meeting)
    return meetings


def update(position: int, meeting_name: str, meeting_day: str, meeting_time: str, zoom_link: str, passcode: int) -> None:
    """
    Update meeting information for existing meeting in database.
    """
    if None not in (meeting_name, meeting_day, meeting_time, zoom_link, passcode):
        meeting_db.update({'meeting_name': meeting_name,
                           'meeting_day': meeting_day,
                           'meeting_time': meeting_time,
                           'zoom_link': zoom_link,
                           'passcode': passcode},
                          MeetingQuery.position == position)
    elif meeting_name is not None:
        meeting_db.update({'meeting_name': meeting_name},
                          MeetingQuery.position == position)
    elif meeting_day is not None:
        meeting_db.update({'meeting_day': meeting_day},
                          MeetingQuery.position == position)
    elif meeting_time is not None:
        meeting_db.update({'meeting_time': meeting_time},
                          MeetingQuery.position == position)
    elif zoom_link is not None:
        meeting_db.update({'zoom_link': zoom_link},
                          MeetingQuery.position == position)
    elif passcode is not None:
        meeting_db.update({'passcode': passcode},
                          MeetingQuery.position == position)


def delete(position) -> None:
    """
    Remove meeting from database.
    """
    count = len(meeting_db)
    meeting_db.remove(MeetingQuery.position == position)
    for pos in range(position + 1, count + 1):
        change_position(pos, pos - 1)

    # Remove the corresponding entry from each contact's 'participation' list.
    results = contact_db.all()
    for result in results:
        participation_list = result['participation']
        participation_list.pop(position - 1)
        contact_db.update({'participation': participation_list}, ContactQuery.position == result['position'])


def change_position(old_position: int, new_position: int) -> None:
    """
    Change position of meeting in database.
    """
    meeting_db.update({'position': new_position},
                      MeetingQuery.position == old_position)


def add_participant(contact_position: int, meeting_position: int) -> None:
    """
    Assigns a contact as a meeting participant. The participant list for 'contact_position' is obtained,
    then the value at the index corresponding to 'meeting_position' is checked. If True, print error.
    Otherwise, change the value and commit the change to the database.
    """
    # Meetings are numbered starting from 1. List indices start from zero. Making sure to change the right meeting:
    ind = meeting_position - 1
    participation = contact_db.search((ContactQuery['position'] == contact_position))[0]['participation']
    if participation[ind]:
        print(f"[red]This contact is already a participant in meeting[/red] {meeting_position}")
    else:
        participation[ind] = not participation[ind]
    contact_db.update({'participation': participation}, ContactQuery.position == contact_position)


def delete_participant(contact_position: int, meeting_position: int) -> None:
    """
    Un-assigns a contact as meeting participant. The participant list for 'contact_position' is obtained,
    then the value at the index corresponding to 'meeting_position' is checked. If True, change it.
    Otherwise, print an "OK" message. The program doesn't care if the user tries to remove what isn't there.
    """
    # Meetings are numbered starting from 1. List indices start from zero. Making sure to change the right meeting:
    ind = meeting_position - 1
    participation = contact_db.search((ContactQuery['position'] == contact_position))[0]['participation']
    if participation[ind]:
        participation[ind] = not participation[ind]
    else:
        print(f"[green]This contact is no longer a participant in meeting[/green] {meeting_position}")
    contact_db.update({'participation': participation}, ContactQuery.position == contact_position)


def read_participants(meeting_position: int) -> List[Tuple[str, str]]:
    ind = meeting_position - 1
    participants = []
    results = contact_db.all()
    for result in results:
        participation_list = result['participation']
        if participation_list[ind]:
            participants.append((result['first_name'], result['last_name']))
    return participants
