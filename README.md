# taRemind:

Provides a simple CLI tool for managing contacts and meetings, and automates the sending of reminder emails.

### Author:

Zane Gerber

### Last Modified:

May 15, 2023

### Status:

Tested and working:

* Contact management     (create, remove, update, read)

* Meeting management     (create, remove, update, read)

* Participant management (assign, release, read)

* Email creation (create and send emails to meeting participants)

To do:

* Documentation. 

* Minor bug fixes
  
## Requirements:

Tested with python 3.8.10 on Ubuntu 20.0.4
	
* typer   
```bash
pip install "typer[all]"
```
* tinydb   
```bash
pip install tinydb
```
* rich 
```bash
pip install rich
```

You will also need a Google 2FA password. See Setup. (This is only necessary if sending emails).

## Setup

This program is designed to send emails from any address, using Gmail as a relay service. This prevents emails from being flagged as spam. You will need a Google account and a 2FA key.

You will also need to set an environment variable to point the program to the 2FA key file. Edit your ~/.bashrc file to include the following line:

```bash
export GMAIL_PASSWORD="your_password"
```	

Be sure to add the location of the program to PATH:

```shell
export PATH=$PATH:/full/path/to/taRemind
```

(Or edit the file containing PATH to include /full/path/to/taRemind. For ubuntu 20.0.4 this file is /etc/environment)
	
## Usage:

See 
```bash
taRemind.py --help
```
	
## Design:

Contacts and meetings are stored in separate databases in JSON format. These databases are built, queried, and edited using tinyDB. The databases are initialized by the 'contacts/\_\_init\_\_.py' and 'meetings/\_\_init\_\_.py' scripts.

Currently, there are classes for Contacts and Meetings.
The attributes of the Contact class are:

* First name

* Last name

* Email address

* Position

The attributes of the Meeting class are:

* Meeting name
	    
* Meeting day
	    
* Meeting time
	    
* Zoom link
	    
* Passcode (optional. Use --passcode if desired.)
	    
* Position
	    
Note that both classes have a 'position' attribute. This is how values will typically be accessed and modified.

For example:
```bash
taRemind.py meetings assign 8 4
```

This line would assign contact #8 to meeting #4.

__I hope to improve this functionality by allowing the user to enter first/last name and meeting name instead of position__

## A good starting place:

The position number of a particular contact can be found by using:

```bash
taRemind.py contacts show
```
	    
The position number of a particular meeting can be found by using:
	
```bash
taRemind.py meetings show
```

