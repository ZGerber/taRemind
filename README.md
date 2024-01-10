# taRemind:

Provides a simple command line tool for managing contacts and meetings, and automates the sending of reminder emails.

## Description
This program is used to manage contacts and meetings, and to send automated email reminders to meeting participants. 

Contacts are stored in a database called contact-book, which is in the JSON format.  Contacts can be added, deleted, or edited, and the contact book can be printed to the console. 

Similarly, meetings are stored in a database called meeting-book, also in the JSON format. Meetings can be created, deleted, or edited, and the meeting book can be printed to the console. 

Contacts can be assigned to (or released from) meetings. If assigned, contacts become 'participants'. Participants will  receive email reminders regarding their upcoming meetings.

Reminders are scheduled within the program. The scheduler runs as a background daemon using Supervisord. Emails can be sent from any address, but Gmail is used as a relay service. 

## Getting Started
                                                               
### Dependencies
Typer: for handling command line input   
```bash
pip install "typer[all]"
```
TinyDB: lightweight database tool
```bash
pip install tinydb
```
Rich: provides output formatting tools
```bash
pip install rich
```

### Installation & Setup
TO DO
### Usage
The user can interact with each database through the command line. The syntax is 
```bash
taremind.py {action} {database}
```
Available commands are:
* show
* add
* delete
* edit

Available databases are:
* contacts
* meetings
* reminders

There are additional commands for assigning (releasing) participants to (from) meetings. These commands do not require a 'database' argument.
* assign
* release

#### Viewing a database
To view the contents of a database, the use the "show" command. For example:
```bash
taremind.py show meetings
```
#### Adding to a database
To add to a database, use the "add" command. For example:
```bash
taremind.py add contact
```
#### Deleting from a database
To delete information from a database, use the "delete" command. For example:
```bash
taremind.py delete contact
```
#### Editing contents of a database
To edit information in a database, use the "edit" command. For example:
```bash
taremind.py edit reminder
```
In addition to these databases, the program can also manage meeting participants. Meeting participation is an attribute of each contact, but the information can be accessed in a way that is consistent with the previous syntax.
#### View meeting participants
```bash
taremind.py show participants
```
This command will give the user two options. You can either view all the participants for a particular meeting, or all the meetings for a particular participant.

#### Assign a participant
```bash
taremind.py assign
```
Then follow the prompts. Contacts can be assigned to multiple meetings at the same time.
#### Release a participant
```bash
taremind.py release
```
Then follow the prompts. Contacts can be released from multiple meetings at the same time.

#### Start the scheduler
The final command is "start"
```bash
taremind.py start
```
This command tells the scheduler to 'activate' all reminders. This command is typically called by Supervisord, a service that runs the process as a background daemon. If the program is properly configured, the user shouldn't need to run this command manually.

## Help

See 
```bash
taremind.py --help
```

Database names can be abbreviated to save typing. For example,
```bash
taremind.py show c
```
will print the contact book to the console.

## Authors

Zane Gerber
zane.gerber@utah.edu

Originally designed for internal use by the Telescope Array Collaboration.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details

