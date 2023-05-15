#!/usr/bin/env python

from typing import List
from models.taRemind_models import Contact, Meeting
from contacts import contact_db, ContactQuery
from meetings import meeting_db, MeetingQuery
from rich import print
from tinydb.operations import delete as dbdel


def create(contact: Contact) -> None:
    """
    Inserts a new contact into the database.
    """
    meeting_count = len(meeting_db)
    contact.position = len(contact_db) + 1
    new_contact = {
        'first_name': contact.first_name,
        'last_name': contact.last_name,
        'email_address': contact.email_address,
        'position': contact.position,
        'participation': [False] * meeting_count  # New contacts aren't participants in any meetings by default
    }
    contact_db.insert(new_contact)
    print("[bold green]DONE![/bold green]")


def read() -> List[Contact]:
    """
    Returns a list of all contacts in the database.
    """
    results = contact_db.all()
    contacts = []
    for result in results:
        contact = Contact(result['first_name'],
                          result['last_name'],
                          result['email_address'],
                          result['position'])
        contacts.append(contact)
    return contacts


def update(position: int, first_name: str, last_name: str, email_address: str, participation: bool = False) -> None:
    """
    Updates contact information for existing contact in the database.
    """
    if None not in (first_name, last_name, email_address):
        contact_db.update({'first_name': first_name,
                           'last_name': last_name,
                           'email_address': email_address},
                          ContactQuery.position == position)
    elif first_name is not None:
        contact_db.update({'first_name': first_name},
                          ContactQuery.position == position)
    elif last_name is not None:
        contact_db.update({'last_name': last_name},
                          ContactQuery.position == position)
    elif email_address is not None:
        contact_db.update({'email_address': email_address},
                          ContactQuery.position == position)
    elif participation:
        # If participation=True, you are adding a new entry to the "participation" list for EACH contact, rather
        # than updating a particular contact. (The "contacts.update()" method is serving multiple purposes in this way.)
        # This only happens when a new meeting is created. Each contact has a list of boolean values corresponding
        # to whether or not the contact is a participant of the i'th meeting, and it needs to be extended by one
        # when the meeting is added. The value of the appended entry is False by default.
        results = contact_db.all()
        for result in results:
            participation_list = result['participation']
            participation_list.append(False)
            contact_db.update({'participation': participation_list}, ContactQuery.position == result['position'])


def delete(position) -> None:
    """
    Removes contact from the database.
    """
    count = len(contact_db)
    contact_db.remove(ContactQuery.position == position)
    for pos in range(position + 1, count + 1):
        change_position(pos, pos - 1)


def change_position(old_position: int, new_position: int) -> None:
    """
    Changes position of contact in the database.
    """
    contact_db.update({'position': new_position},
                      ContactQuery.position == old_position)
