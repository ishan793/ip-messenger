# Function Definitions Guide for Graphical User Interface

![GUI Overview Diagram](https://bitbucket.org/mshekhar/ipmessenger/src/master/GUI.png)

## Class Chatscreen():
This class creates the chat screen frame. The chat screen frame displays the text messages from the user whose screen has opened through a button in the parent frame. It also has a text control for sending messages
    *	Input: wx.Frame

  1. __init__
  The function initializes the attributes of the chat screen frame and also calls all the functions required to define the properties of various frame controls. It also has subscriber initialised to run a thread continuously.
    *	Input: self, user, passw, friend, *args, **style
  
  2. Method OnClose: Destroys the window
    *	Inputs: self, event
  
  3. Method __set_chatlog: Loads the text to display on the text control screen.
    *	Inputs: self, msg1
  
  4. Method __set_properties: Sets the properties of the text control frame.
    *	Inputs: self
  
  5. Method __do_layout: Sets the layout and properties of the sizer of the frame.
    *	Inputs: self
  
  6. Method text_e: Records the text entered in the text control box. Appends the text to the messages history. Also, loads the text screen again with the new messages.
    *	Inputs: self, event

## Class OnlineOfflineThread():
  This class initializes and runs a thread which updates the chatroom after every 10 seconds.
  
  1. __init__
  This function initializes the thread which updates the chatroom after every 10 seconds.
    *	Input: self
	
  2. __init__
  This function runs the thread which updates the chatroom after every 10 seconds. It also publishes a message to the class which will update the chatroom.
    *	Input: self
	
## Class OnlineOfflineScreen():
	This class creates the graphical layout of the chatroom.	
	
  1.	Method init: This function sets the dimensions of the frame and the layout of the buttons
    *		Inputs: self, user, passw
	
  2.	Method OnCloseMe: destroys the window
    *		Inputs: self
	
  3.	Method updateButton: This method refreshes the chatroom window with button updates
    *		Inputs: self, msg
	
  4.	Method createButton: This method gets a dictionary of online/offline users. After iterating through the dictionary, it creates a green button to indicate and online user and normal button to indicate offline user.
    *		Inputs: self, msg
	
  5.	Method OnB: This method contains an event handler which opens a specific chat window of the person whose button is pressed
    *		Inputs: self, event

## 	Class chat_login: 
	This class creates login screen of the chat application
    *	Inputs: wx.App

## 	Class login_panel: 
	This class uses the authenticate method to redirect the user to chatroom if the username and password entered is correct
    *	Inputs: wx.Frame
	