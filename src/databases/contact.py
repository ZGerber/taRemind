#!/usr/bin python3

import typer
import common.user_prompts as UserPrompt
from typing import List
from dataclasses import dataclass, field
from databases.database import Database
from databases import ContactQuery, ContactDatabase, MeetingDatabase, console
from rich.prompt import Prompt as p
from rich.table import Table
from rich import print


@dataclass
class Contact(Database):
    contact_attributes: List = field(default_factory=lambda: ["First Name",
                                                              "Last Name",
                                                              "Email Address"])

    def query(self):
        """ Query the entire database
        """
        return ContactDatabase.all()

    def display(self):
        """  Display a table of all contacts.
        """
        results = self.query()
        if not results:
            print("[red]No contacts found![/red]")
            typer.Abort()
        table = self.configure_table()
        self.fill_table(table, results)
        console.print(table)

    def add(self):
        """ Add contact to the database
        """
        first_name, last_name, email_address = UserPrompt.add_contact()
        meeting_count = len(MeetingDatabase)
        position = len(ContactDatabase) + 1
        new_contact = {
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address,
            'position': position,
            'participation': [False] * meeting_count  # New contacts aren't participants in any meetings by default
        }
        UserPrompt.confirm("add_contact", first_name, last_name, email_address)
        ContactDatabase.insert(new_contact)
        return

    def delete(self):
        """ Remove a contact from the database
        """
        person = UserPrompt.delete_contact(self.get_names())
        if not person:
            self.display()
        else:
            pos = self.get_position(person['name'])
            UserPrompt.confirm("delete_contact", pos)
            ContactDatabase.remove(ContactQuery.position == pos)
            self.reset_positions(pos)

    def edit(self):
        person, attribute = UserPrompt.edit_contact(self.get_names(), self.contact_attributes)
        if not person:
            self.display()
        else:
            pos = self.get_position(person['name'])
            if attribute["attribute"] == "First Name":
                ContactDatabase.update({'first_name': p.ask("Enter the new First Name for this contact")},
                                       ContactQuery.position == pos)
            elif attribute["attribute"] == "Last Name":
                ContactDatabase.update({'last_name': p.ask("Enter the new Last Name for this contact")},
                                       ContactQuery.position == pos)
            elif attribute["attribute"] == "Email Address":
                ContactDatabase.update({'email_address': p.ask("Enter the new Email Address for this contact")},
                                       ContactQuery.position == pos)
            print(f"[green]SUCCESS![/green]")

    @staticmethod
    def get_position(entry) -> int:
        """ Gets a single entry from the contact database. Returns the position number of that entry.
        Can accept either FIRST and LAST name, or POSITION.
        """
        if entry.isdigit():
            position = entry
        else:
            first_name = entry.split()[0]
            last_name = entry.split()[1]
            position = ContactDatabase.get((ContactQuery.first_name == first_name
                                            and ContactQuery.last_name == last_name))['position']
        if not position:
            print("[red]ERROR: Invalid entry.[/red]")
            raise typer.Exit()
        return int(position)

    @staticmethod
    def change_position(old_position: int, new_position: int) -> None:
        """ Changes position of contact in the database.
        """
        ContactDatabase.update({'position': new_position},
                               ContactQuery.position == old_position)

    def reset_positions(self, pos):
        """ After deleting a contact, the positions need to be reset to keep them contiguous.
        """
        for i in range(pos + 1, len(self.query()) + 2):
            self.change_position(i, i - 1)

    @staticmethod
    def configure_table():
        """ Set up the table for displaying contacts
        """
        table = Table(show_header=True, show_lines=True)
        table.add_column("Position", width=8, justify="center")
        table.add_column("Name", min_width=20, justify="center")
        table.add_column("Email Address", min_width=20, justify="center")
        return table

    @staticmethod
    def fill_table(table, results):
        """ Populate the table for displaying contacts
        """
        for contact in results:
            table.add_row(f"[cyan]{contact['position']}[/cyan]",
                          f"[bold]{contact['first_name']} {contact['last_name']}[/bold]",
                          f"{contact['email_address']}")

    def get_names(self):
        """ Return a list of all contact names
        """
        return [(result['first_name'] + " " + result['last_name']) for result in self.query()]
