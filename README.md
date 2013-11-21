# ipMessenger

## Python Project
This repository contains code for a LAN based chat messenger written specifically for IIT Gandhinagar Network that is independent of any Internet requirement. The entire application has been written in Python.

## About the Application
iPMessenger is Request based chat messenger. Each active client selects another client whom it want to send a chat message. A Django based server at the back-end collects that message and forwards it to appropriate receiver. 
The application contains two major parts:
### Back-end
  * Let's the first time user register for the service.
  * Collects the message from and client, and send relays that to receiver in JSON format.
  * Let's the GUI know which users are online and how many new messages has he received while he was off-line.
### Front-end or Graphical User Interface
  * Redirects first-timers to Sign-Up page.
  * Let user Sign in and see which other users are online and how many new messages has he/she received.
  * Clicking on a user lets him see his previous chat messages, time of receiving those messages. It also lets user chat with the other person.


## Requirement
Application users have the following dependencies installed on their computers:

* Python 2.7.x 
* wxPython: Library for GUI related tasks.
* Django: For developers who want to modify backend related tasks.


## Quick Start
1. Clone the git repo `git clone https://bitbucket.org/mshekhar/ipmessenger.git`
2. Install the required dependencies.
3. Double click and run the 'PingYu.py' file.


## Documentation
* [Backend](https://bitbucket.org/mshekhar/ipmessenger/src/master/Backend.md)
* [Frontend](https://bitbucket.org/mshekhar/ipmessenger/src/master/GUI.md)

## Contributing
Anyone and everyone is welcome to download or contribute. Future plan includes:

### Better GUI
  * A better more intuitive Graphical User Interface, with split screen chat window. The chat window could also display chat messages in Rich text format instead of plain text.

### ipMessenger for Android
  * Port the messenger to the Android platform.