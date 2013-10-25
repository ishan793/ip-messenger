import wx
import wx.lib.buttons as buttons

class GenericButtonFrame(wx.Frame):
    def __init__(self,d):
        wx.Frame.__init__(self, None, -1, 'Generic Button Example', 
                size=(500, 350))
        panel = wx.Panel(self, -1)
        
        sizer = wx.FlexGridSizer(6, 1, 0, 20)
        
        self.createButton()
    def createButton(self):
        a=self.d
        for key in a:
            if(a[key]==1):
                b = wx.Button(panel, -1, key) #creates a button
                b.SetDefault()
                sizer.Add(b)
                panel.SetSizer(sizer)
                
            elif(a[key]==0):
                b = buttons.GenButton(panel, -1, key)
                b.Enable(False)
                sizer.Add(b)
                panel.SetSizer(sizer)
    
    
        
if __name__ == '__main__':
    d = {'Vinit Joshi':1, 'Nandan Vora':0}
    
    app = wx.PySimpleApp()
    frame = GenericButtonFrame(d)
    frame.Show()
    app.MainLoop()        
