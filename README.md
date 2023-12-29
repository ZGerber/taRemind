# taRemind:

Provides a simple CLI tool for managing contacts and meetings, and automates the sending of reminder emails.

### Author:

Zane Gerber

### Last Modified:

May 10, 2023

### Status:

Tested and working:

* Contact management     (create, remove, update, read)

* Meeting management     (create, remove, update, read)

* Participant management (assign, release, read)

To do:

* Documentation. Add help strings, annotations, etc. Make it pretty.

* Add functionality to send emails. This will be incorporated as a separate python module.
The sending of emails depends on successful authentication of DNS records. CHPC has made the changes, and I am
waiting for them to take effect.
  
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
* sendgrid 
```bash
pip install sendgrid
```

You will also need a Sendgrid API key. See Setup. (This is only necessary if sending emails).

## Setup

For sending emails from ta-remind@cosmic.utah.edu, the sendgrid API key has already been obtained (ask Zane). DO NOT DELETE this key without good reason. 

If you wish to use this program to send emails from some other domain, you will need a new Sendgrid account and API key.

You will need to set an environment variable to point the program to the API key file. Edit your ~/.bashrc file to include the following line:

```bash
export SENDGRID_API_KEY=/full/path/to/taRemind/sendgrid_api_key.txt
```

Be sure to add the location of the program to PATH:

```bash
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

## A good starting place:

The position number of a particular contact can be found by using:

```bash
taRemind.py contacts show
```
	    
The position number of a particular meeting can be found by using:
	
```bash
taRemind.py meetings show
```

