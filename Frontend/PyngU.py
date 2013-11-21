import wx
from parse_online import *
from wx.lib.scrolledpanel import ScrolledPanel
import authenticate
import messages_frontEnd as mf
import os
import time
from threading import Thread
from wx.lib.pubsub import Publisher

class ChatScreen(wx.Frame):
    """This class creates the chat screen frame. The chat screen frame displays
    the text messages from the user whose screen has opened through a button in
    the parent frame. It also has a text control for sending messages."""
    def __init__(self, user, passw, friend, *args, **style):
        """The functions initializes the attributes of the chat screen frame and
        also calls all the functions required to define the properties of various
        frame controls. It also has subscriber initialised to run a thread
        continuously."""
        style["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **style)
        self.chat_log = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_send = wx.TextCtrl(self, -1, "")
        self.user=user
        self.passw=passw
        self.friend=friend
        self.__set_properties()
        self.__do_layout()
        self.__set_chatlog(0)
        self.Bind(wx.EVT_TEXT_ENTER, self.text_e, self.text_send)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        Publisher().subscribe(self.__set_chatlog, "updatetext")

    def OnClose(self, event):
        """Destroys the frame."""
        self.Destroy()
        

    def __set_chatlog(self, msg1):
        """Loads the text to display on the text control screen."""
        directory=os.getcwd()+ '/messages'
        filename=str(self.user)+'_'+str(self.friend)
        messages = mf.getMessage(self.user, self.friend, self.passw)
        mf.makeTextFile(self.user, self.friend, self.passw, messages)
        self.chat_log.LoadFile('/'.join((directory, filename)))
        self.chat_log.ShowPosition(self.chat_log.GetLastPosition())
        
    def __set_properties(self):
        """Sets the properties of the text control frame.""" 
        self.SetTitle(str(self.friend))
        self.SetSize((653, 467))
        self.chat_log.SetMinSize((635, 400))
        self.text_send.SetMinSize((635, -1))
        self.text_send.SetFocus()
        

    def __do_layout(self):
        """Sets the layout and properties of the sizer of the frame."""
        sizer_1 = wx.FlexGridSizer(1, 1, 1, 1)
        sizer_1.Add(self.chat_log, 0, 0, 0)
        sizer_1.Add(self.text_send, 0, wx.ALL, 1)
        self.SetSizer(sizer_1)
        self.Layout()
        

    def text_e(self, event):
        """Records the text entered in the text control box. Appends the
        text to the messages history. Also, loads the text screen again with
        the new messages."""
        directory=os.getcwd()+ '/messages'
        filename=str(self.user)+'_'+str(self.friend)
        text = self.text_send.GetValue()
        messages = mf.addMessage(self.user, self.friend, self.passw, text)
        mf.makeTextFile(self.user, self.friend, self.passw, messages)
        
        self.chat_log.LoadFile('/'.join((directory, filename)))
        self.text_send.SetValue("")
        event.Skip()

class OnlineOfflineThread(Thread):
    """This class initializes and runs a thread which updates the chatroom
    after every 10 seconds."""
    def __init__(self):
        """This function initializes the thread which updates the chatroom
        after every 10 seconds."""
        Thread.__init__(self)
        self.start()
        
    def run(self):
        """This function runs the thread which updates the chatroom
        after every 10 seconds. It also publishes a message to the class
        which will update the chatroom."""
        run=0
        wx.CallAfter(Publisher().sendMessage, "update", "")
        time.sleep(10)
        while (run==0):
            wx.CallAfter(Publisher().sendMessage, "updatebuttons", "")
            time.sleep(10)
            
        
class TextThread(Thread):
    """This class initializes and runs a thread which updates the chat screen
    after every 3 seconds."""
    def __init__(self):
        """This function initializes the thread which updates the chat screen
        after every 3 seconds."""
        Thread.__init__(self)
        self.start()
        
    def run(self):
        """This function runs the thread which updates the chat screen
        after every 3 seconds. It also publishes a message to the class
        which will update the chat screen."""
        run1=0
        while (run1==0):
            Publisher().sendMessage("updatetext", "")
            time.sleep(3)
        
class OnlineOfflineScreen(wx.Frame):
    """This class creates the graphical layout of the chatroom"""
    def __init__(self,user,passw):
        """This function sets the dimensions of the frame and
        the layout of the buttons"""
        self.user = user
        self.passw=passw
        wx.Frame.__init__(self, None, -1, 'Friends', 
                size=(500, 350))
        self.panel = ScrolledPanel(self, size = wx.Size( 500, 350 ))
        self.panel.SetupScrolling()
        self.Bind(wx.EVT_CLOSE, self.OnCloseMe)
        self.sizer = wx.FlexGridSizer(5,2,5,5)
        self.buttons=[]
        Publisher().subscribe(self.createButton, "update")
        Publisher().subscribe(self.updateButton, "updatebuttons")
        

    def OnCloseMe(self, event):
        """destroys the window"""
        self.Destroy()

    def updateButton(self, msg):
        """This method refreshes the chatroom window with button updates"""
        onoffdict = online_users(chat_login.UserText,chat_login.PasswordText)
        unreadmessages = unread_messages(chat_login.UserText,chat_login.PasswordText)
        a=onoffdict
        u=unreadmessages
        for key in a:
            KeyFound = False
            for button in self.buttons:
                if (button.parameterVal==key):
                    KeyFound = True
                    if(a[key]==1):
                        button.SetBackgroundColour('#89E398')
                    elif a[key]==0:
                        button.SetBackgroundColour('#E6E6E6')
                    if(u[key]==0):
                        button.SetLabel(key) 
                    else:
                        button.SetLabel(key+' ('+str(u[key])+')')

            if (KeyFound==False):
                if(self.user==key):
                    pass
                else:
                    if(a[key]==1):
                        if(u[key]==0):
                            b = wx.Button(self.panel, -1, key) 
                        else:
                            b = wx.Button(self.panel, -1, key+' ('+str(u[key])+')')
                        self.buttons.append(b)
                        b.Enable(True)
                        b.SetBackgroundColour('#89E398') 
                        self.sizer.Add(b,0,wx.EXPAND)
                        b.parameterVal=key
                        b.Bind(wx.EVT_BUTTON,self.OnB)
                        self.panel.SetSizer(self.sizer)
                        w, h = self.GetClientSize()
                        self.SetSize((w, h))
                        self.Show()
                        
                    elif(a[key]==0):
                        if(u[key]==0):
                            b = wx.Button(self.panel, -1, key) 
                        else:
                            b = wx.Button(self.panel, -1, key+' ('+str(u[key])+')')
                        self.buttons.append(b)
                        b.Enable(True)
                        button.SetBackgroundColour('#E6E6E6')
                        self.sizer.Add(b,0,wx.EXPAND)
                        b.parameterVal=key
                        b.Bind(wx.EVT_BUTTON,self.OnB)
                        self.panel.SetSizer(self.sizer)
                        w, h = self.GetClientSize()
                        self.SetSize((w, h))
                        self.Show()
                
            
    def createButton(self, msg):
        """This method gets a dictionary of online/offline users. After iterating
            through the dictionary, it creates a green button to indicate an
            online user and normal button to indicate offline user"""
        onoffdict = online_users(chat_login.UserText,chat_login.PasswordText)
        unreadmessages = unread_messages(chat_login.UserText,chat_login.PasswordText)
        a=onoffdict
        u=unreadmessages
        for key in a:
            if(self.user==key):
                pass
            else:
                if(a[key]==1):
                    if(u[key]==0):
                        b = wx.Button(self.panel, -1, key) 
                    else:
                        b = wx.Button(self.panel, -1, key+' ('+str(u[key])+')')
                    self.buttons.append(b)
                    b.Enable(True)
                    b.SetBackgroundColour('#89E398') 
                    self.sizer.Add(b,0,wx.EXPAND)
                    b.parameterVal=key
                    b.Bind(wx.EVT_BUTTON,self.OnB)
                    self.panel.SetSizer(self.sizer)
                    
                elif(a[key]==0):
                    if(u[key]==0):
                        b = wx.Button(self.panel, -1, key) 
                    else:
                        b = wx.Button(self.panel, -1, key+' ('+str(u[key])+')')
                    self.buttons.append(b)
                    b.Enable(True)
                    b.SetBackgroundColour('#E6E6E6')
                    self.sizer.Add(b,0,wx.EXPAND)
                    b.parameterVal=key
                    b.Bind(wx.EVT_BUTTON,self.OnB)
                    self.panel.SetSizer(self.sizer)
        self.Centre()
        self.Show()
        
    def OnB(self, event):
        """This method contains an event handler which opens a specific chat
            window of the person whose button is pressed"""
        bp = event.GetEventObject()
        friend = bp.parameterVal
        app1 = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        frame_1 = ChatScreen(self.user, self.passw,friend, None, -1, "")
        TextThread()
        app1.SetTopWindow(frame_1)
        frame_1.Show()
        app1.MainLoop()
        
class chat_login(wx.App):
    """This class creates login screen of the chat application"""
    UserText=''
    PasswordText=''
    def OnInit(self):
        frame = login_frame (None, 0, "Chat Login")
        frame.Show()
        self.SetTopWindow(frame)

        loginPanel = login_panel(frame)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
        return True

    def OnCloseWindow(self, event):
        self.Destroy()

class login_frame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, wx.DefaultPosition,wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
        self.CreateStatusBar()
        self.Bind(wx.EVT_CLOSE, self.OnCloseMe)

    def OnCloseMe(self, event):
        self.Destroy()

class login_panel(wx.Panel):
    """This class uses the authenticate method to redirect the user to chatroom if
        if the username and password entered is correct"""
    def __init__(self, frame):  
        self.panel = wx.Panel(frame)
        self.frame = frame

        self.frame.SetStatusText("Authentication required!")
        self.showLoginBox() 

    def showLoginBox (self):
        sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=15)

        self.txt_Username = wx.TextCtrl(self.panel, 1, size=(150, -1))
        Username_label = wx.StaticText(self.panel, -1, "Username:")
        sizer.Add(Username_label,0, wx.LEFT|wx.TOP| wx.RIGHT, 50)
        sizer.Add(self.txt_Username,0, wx.TOP| wx.RIGHT, 50)

        self.txt_Password = wx.TextCtrl(self.panel, 1, size=(150, -1), style=wx.TE_PASSWORD)
        Password_label = wx.StaticText(self.panel, -1, "Password:")
        sizer.Add(Password_label,0, wx.LEFT|wx.RIGHT, 50)
        sizer.Add(self.txt_Password,0, wx.RIGHT, 50)

        submit_button = wx.Button(self.panel, -1, "Login")
        self.panel.Bind(wx.EVT_BUTTON, self.OnSubmit, submit_button)
        sizer.Add(submit_button,0, wx.LEFT, 50)

        signup_button = wx.Button(self.panel, -1, "Sign Up")
        self.panel.Bind(wx.EVT_BUTTON, self.OnSignup, signup_button)
        sizer.Add(signup_button,0, wx.LEFT, 50)

        self.panel.SetSizer(sizer)

    def OnSignup(self, event):
        """This method redirects the user to a webpage to sign up for the chat
            application"""
        href="http://192.168.7.250:8000/signup/"
        wx.BeginBusyCursor() 
        import webbrowser 
        webbrowser.open(href) 
        wx.EndBusyCursor() 


    def OnSubmit(self, event):
        """This class uses the authenticate method to redirect the user to chatroom if
        if the username and password entered is correct"""
        chat_login.UserText = self.txt_Username.GetValue()
        chat_login.PasswordText = self.txt_Password.GetValue()
        flag=authenticate.authenticate(chat_login.UserText,chat_login.PasswordText)
        if flag==0:
            self.frame.SetStatusText("Sorry")
        elif flag==2:
            self.frame.SetStatusText("Username not registered")
        elif flag==1:
            self.frame.Close(True)
            app = wx.App(True)
            OnlineOfflineScreen(chat_login.UserText, chat_login.PasswordText)
            OnlineOfflineThread()

            app.MainLoop()
if __name__ == '__main__':
    appmain = chat_login()
    appmain.MainLoop()
