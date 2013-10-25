import wx

 ########################################################################
class MyFrame(wx.Frame):
    def __init__(self, *args, **style):
        style["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **style)
        self.chat_log = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_send = wx.TextCtrl(self, -1, "")

        self.__set_properties()
        self.__do_layout()
        self.__set_chatlog()
        self.Bind(wx.EVT_TEXT_ENTER, self.text_e, self.text_send)
        

    def __set_chatlog(self):
        directory='C:\Users\Manish\Desktop'
        filename='test.txt' 
        self.chat_log.LoadFile('/'.join((directory, filename)))
        
    def __set_properties(self):
        
        self.SetTitle("ChatBox")
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
        filename='test.txt'
        filename1='test1.txt'
        
        
        fh=open('/'.join((directory, filename)),"a+")
        text = self.text_send.GetValue()
        fh.write("\n"+text)
        fh.flush()
        fh.close()
        
        self.chat_log.LoadFile('/'.join((directory, filename)))
        self.text_send.SetValue("")
        event.Skip()


 ########################################################################
class Prototype(wx.Frame):

      #----------------------------------------------------------------------
      def __init__(self, parent, title):
           wx.Frame.__init__(self, None, title="First Frame", size=(1240,705))
           self.UI()
           self.Centre()
           self.Show()

      #----------------------------------------------------------------------
      def UI(self):
           self.panel1 = wx.Panel(self, -1)
           self.sizer = wx.BoxSizer()
           self.sizer.Add(self.panel1, 1, flag=wx.EXPAND) 
           b = wx.Button(self.panel1, label='second window', size=(180,100), pos=(650,25))
           b.Bind(wx.EVT_BUTTON, self.OnB)        

           self.SetSizer(self.sizer)  

      #----------------------------------------------------------------------
      def OnB(self, event):
        app1 = wx.PySimpleApp(0)
        wx.InitAllImageHandlers()
        frame_1 = MyFrame(None, -1, "")
        app1.SetTopWindow(frame_1)
        frame_1.Show()
        app1.MainLoop()

 #----------------------------------------------------------------------
app = wx.App(False)
Prototype(None, title='')
app.MainLoop()
