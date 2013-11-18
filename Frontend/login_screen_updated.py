import wx
from wx.lib.scrolledpanel import ScrolledPanel
import authenticate
onoffdict = {'Vinit Joshi':1, 'Nandan Vora':0,'Raj Shah':1,'Vinit Joshiq':1, 'Nandaxn Vora':0,'Racj Shah':0,
                 'Vinidt Joshi':1, 'Nanddan Vora':0,'Raj Shachs':0, 'Vdinit Joshi':1,
                 'Nandan Vgtora':0,'Raj Sdhah':1,'Vinit Jos1hiq':1, 'Nan1daxn Vora':0,'Ra1cj Shah':0,
                 'Vinidt Jos1hi':1, 'Nan1ddan Vora':0,'Raj Shac1h':0}
 ########################################################################
class ChatScreen(wx.Frame):
    def __init__(self, user, friend, *args, **style):
        style["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **style)
        self.chat_log = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_send = wx.TextCtrl(self, -1, "")
        self.user=user
        self.friend=friend
        self.__set_properties()
        self.__do_layout()
        self.__set_chatlog()
        self.Bind(wx.EVT_TEXT_ENTER, self.text_e, self.text_send)
        

    def __set_chatlog(self):
        directory='C:\Users\Manish\Desktop'
        if (self.user<self.friend):
            filename=str(self.user)+'_'+str(self.friend)
        else:
            filename=str(self.friend)+'_'+str(self.user)
##        filename='test.txt'
        fh=open('/'.join((directory, filename)),"a+")
        fh.close()
        self.chat_log.LoadFile('/'.join((directory, filename)))
        
    def __set_properties(self):
        
        self.SetTitle(str(self.friend))
        self.SetSize((653, 467))
        self.chat_log.SetMinSize((635, 400))
        self.text_send.SetMinSize((635, -1))
        self.text_send.SetFocus()
        

    def __do_layout(self):
        
        sizer_1 = wx.FlexGridSizer(1, 1, 1, 1)
        sizer_1.Add(self.chat_log, 0, 0, 0)
        sizer_1.Add(self.text_send, 0, wx.ALL, 1)
        self.SetSizer(sizer_1)
        self.Layout()
        

    def text_e(self, event):
        directory='C:\Users\Manish\Desktop'
##        filename='test.txt'
        if (self.user<self.friend):
            filename=str(self.user)+'_'+str(self.friend)
        else:
            filename=str(self.friend)+'_'+str(self.user)
        fh=open('/'.join((directory, filename)),"a+")
        text = self.text_send.GetValue()
        fh.write("\n"+text)
        fh.flush()
        fh.close()
        
        self.chat_log.LoadFile('/'.join((directory, filename)))
        self.text_send.SetValue("")
        event.Skip()


 ########################################################################
class OnlineOfflineScreen(wx.Frame):
    def __init__(self,user,dictionary):
        self.d=dictionary
        self.user = user
        wx.Frame.__init__(self, None, -1, 'Friends', 
                size=(500, 350))
        self.panel = ScrolledPanel(self, size = wx.Size( 600, 400 ))
        self.panel.SetupScrolling()
        self.boxsizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.FlexGridSizer(5,5,5,5)
        self.createButton()
        self.Centre()
        self.Show()
    def createButton(self):
        a=self.d
        for key in a:
            i=0
            if(a[key]==1):
                b = wx.Button(self.panel, i, key) #creates a button
                b.Enable(True)
                b.SetBackgroundColour('#89E398') 
                self.sizer.Add(b,0,wx.EXPAND)
                b.parameterVal=key
                b.Bind(wx.EVT_BUTTON,self.OnB)
                self.panel.SetSizer(self.sizer)
                
            elif(a[key]==0):
                b = wx.Button(self.panel, i, key)
                b.Enable(True)
                self.sizer.Add(b,0,wx.EXPAND)
                b.parameterVal=key
                b.Bind(wx.EVT_BUTTON,self.OnB)
                self.panel.SetSizer(self.sizer)
        i=i+1
                
    def OnB(self, event):
        bp = event.GetEventObject()
        friend = bp.parameterVal
        app1 = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        frame_1 = ChatScreen(self.user, friend, None, -1, "")
        app1.SetTopWindow(frame_1)
        frame_1.Show()
        app1.MainLoop()
##class Prototype(wx.Frame):
##
##      #----------------------------------------------------------------------
##      def __init__(self, parent, title):
##           wx.Frame.__init__(self, None, title="First Frame", size=(1240,705))
##           self.UI()
##           self.Centre()
##           self.Show()
##
##      #----------------------------------------------------------------------
##      def UI(self):
##           self.panel1 = wx.Panel(self, -1)
##           self.sizer = wx.BoxSizer()
##           self.sizer.Add(self.panel1, 1, flag=wx.EXPAND) 
##           b = wx.Button(self.panel1, label='second window', size=(180,100), pos=(650,25))
##           b.Bind(wx.EVT_BUTTON, self.OnB)        
##
##           self.SetSizer(self.sizer)  
##
##      #----------------------------------------------------------------------
##      def OnB(self, event):
##        app1 = wx.PySimpleApp(0)
##        wx.InitAllImageHandlers()
##        frame_1 = ChatScreen(1234, 2345,None, -1, "")
##        app1.SetTopWindow(frame_1)
##        frame_1.Show()
##        app1.MainLoop()

 #----------------------------------------------------------------------

class chat_login(wx.App):
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

    def OnCloseMe(self, event):
        self.Close(True)

class login_panel(wx.Panel):
    def __init__(self, frame):  
        self.panel = wx.Panel(frame)
        self.frame = frame

        self.frame.SetStatusText("Authentication required!")
        self.showLoginBox() 

    def showLoginBox (self):
        sizer = wx.FlexGridSizer(rows=3, cols=2, hgap=5, vgap=15)

      # Username
        self.txt_Username = wx.TextCtrl(self.panel, 1, size=(150, -1))
        Username_label = wx.StaticText(self.panel, -1, "Username:")
        sizer.Add(Username_label,0, wx.LEFT|wx.TOP| wx.RIGHT, 50)
        sizer.Add(self.txt_Username,0, wx.TOP| wx.RIGHT, 50)

      # Password
        self.txt_Password = wx.TextCtrl(self.panel, 1, size=(150, -1), style=wx.TE_PASSWORD)
        Password_label = wx.StaticText(self.panel, -1, "Password:")
        sizer.Add(Password_label,0, wx.LEFT|wx.RIGHT, 50)
        sizer.Add(self.txt_Password,0, wx.RIGHT, 50)

      # Submit button
        submit_button = wx.Button(self.panel, -1, "Login")
        self.panel.Bind(wx.EVT_BUTTON, self.OnSubmit, submit_button)
        sizer.Add(submit_button,0, wx.LEFT, 50)

        signup_button = wx.Button(self.panel, -1, "Sign Up")
        self.panel.Bind(wx.EVT_BUTTON, self.OnSignup, signup_button)
        sizer.Add(signup_button,0, wx.LEFT, 50)

        self.panel.SetSizer(sizer)

    def OnSignup(self, event):
        href="http://192.168.7.250:8009/signup/"
        wx.BeginBusyCursor() 
        import webbrowser 
        webbrowser.open(href) 
        wx.EndBusyCursor() 


    def OnSubmit(self, event):
        chat_login.UserText = self.txt_Username.GetValue()
        chat_login.PasswordText = self.txt_Password.GetValue()
        flag=authenticate.authenticate(chat_login.UserText,chat_login.PasswordText)
        if flag==0:
            self.frame.SetStatusText("Sorry")
        elif flag==1:
            self.frame.Close(True)
            app = wx.App(False)
            OnlineOfflineScreen(chat_login.UserText, onoffdict)
##            Prototype(None, title='')
            app.MainLoop()
if __name__ == '__main__':
    appmain = chat_login()
    appmain.MainLoop()

    
