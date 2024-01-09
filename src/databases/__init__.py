#!/usr/bin python3
from pathlib import Path

from rich.console import Console
from tinydb import TinyDB, Query

"""
Initializes the databases using TinyDB.
"""

# Set paths to program directories
ROOT_DIR = Path(__file__).parent.parent
DATABASE_DIR = Path(ROOT_DIR, 'databases')
MEETING_DB_NAME = 'meeting-book.json'
MEETING_DB_FILE = Path(DATABASE_DIR, MEETING_DB_NAME)
CONTACT_DB_NAME = 'contact-book.json'
CONTACT_DB_FILE = Path(DATABASE_DIR, CONTACT_DB_NAME)
REMINDER_DB_NAME = 'reminder-book.json'
REMINDER_DB_FILE = Path(DATABASE_DIR, REMINDER_DB_NAME)


# Initialize the MEETING database
MeetingDatabase = TinyDB(MEETING_DB_FILE)
MeetingDatabase.default_table_name = 'meeting-book'
MeetingQuery = Query()

# Initialize the CONTACT database
ContactDatabase = TinyDB(CONTACT_DB_FILE)
ContactDatabase.default_table_name = 'contact-book'
ContactQuery = Query()

# Initialize the REMINDER database
ReminderDatabase = TinyDB(REMINDER_DB_FILE)
ReminderDatabase.default_table_name = 'reminder-book'
ReminderQuery = Query()

# Class for formatting terminal output
console = Console()
