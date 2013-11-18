import wx
import wx.lib.buttons as buttons

class GenericButtonFrame(wx.Frame):
    def __init__(self,dictionary):
        self.d=dictionary
        wx.Frame.__init__(self, None, -1, 'Generic Button Example', 
                size=(500, 350))
        self.panel = wx.Panel(self, -1)
        
        self.sizer = wx.FlexGridSizer(6, 1, 0, 20)
        
        self.createButton()
    def createButton(self):
        a=self.d
        for key in a:
            if(a[key]==1):
                b = wx.Button(self.panel, -1, key) #creates a button
                b.Enable(True)
                b.SetBackgroundColour('#89E398') 
                self.sizer.Add(b)
                self.panel.SetSizer(self.sizer)
                
            elif(a[key]==0):
                b = buttons.GenButton(self.panel, -1, key)
                b.Enable(True)
                self.sizer.Add(b)
                self.panel.SetSizer(self.sizer)
    
    
        
if __name__ == '__main__':
    d = {'Vinit Joshi':1, 'Nandan Vora':0,'Raj Shah':1}
    
    app = wx.PySimpleApp()
    frame = GenericButtonFrame(d)
    frame.Show()
    app.MainLoop()        
