from tinydb import TinyDB, Query
from pathlib import Path
from rich.console import Console
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

# Initialize the MEETING database
MeetingDatabase = TinyDB(MEETING_DB_FILE)
MeetingDatabase.default_table_name = 'meeting-book'
MeetingQuery = Query()  # This object is used to interact with the database

# Initialize the CONTACT database
ContactDatabase = TinyDB(CONTACT_DB_FILE)
ContactDatabase.default_table_name = 'contact-book'
ContactQuery = Query()  # This object is used to interact with the database

console = Console()  # Class for terminal formatting
