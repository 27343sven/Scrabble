import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Scrabble")
        text.SetFont(wx.Font(50, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        boxje.Add(text, 1, wx.CENTER)
        boxje.Add(wx.Panel(self, -1), 1)
        boxje.Add(self.createButtonBox(), 1, wx.ALIGN_CENTER | wx.EXPAND | wx.ALL)
        self.SetSizer(boxje)

    def createButtonBox(self):
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        self.spelenButton = wx.Button(self, 1, "Spel Spelen")
        self.settingsButton = wx.Button(self, 2, "Settings")
        self.scoreButton = wx.Button(self, 3, "Scorebord")
        self.stoppenButton = wx.Button(self, 4, "Stoppen")
        self.buttons = [self.spelenButton, self.settingsButton, self.scoreButton, self.stoppenButton]
        buttonSizer.Add(self.spelenButton, 1, wx.CENTER)
        buttonSizer.AddSpacer(30)
        buttonSizer.Add(self.settingsButton, 1, wx.CENTER)
        buttonSizer.AddSpacer(30)
        buttonSizer.Add(self.scoreButton, 1, wx.CENTER)
        buttonSizer.AddSpacer(30)
        buttonSizer.Add(self.stoppenButton, 1, wx.LEFT)
        return(buttonSizer)


    def center(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.CENTRE)
        return(hbox)

    def left(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.RIGHT)
        return(hbox)

if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(600, 400),
                              style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX)
            boxje = wx.BoxSizer()
            boxje.Add(Schermpje(self, id), 1, wx.EXPAND | wx.ALL, 1)
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(wx.Bitmap("scrabble.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
            self.SetSizer(boxje)
            self.Centre()
            self.Show(True)


    app = wx.App()
    Naampje(None, -1, "Scrabble!")
    app.MainLoop()