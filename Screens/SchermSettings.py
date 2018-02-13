import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Settings")
        text.SetFont(wx.Font(50, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        boxje.Add(text, 1, wx.CENTER)
        boxje.Add(self.makeScherm(), 10, wx.CENTER | wx.EXPAND | wx.ALL)
        boxje.Add(self.makeBackButton(), 1, wx.EXPAND | wx.ALL)
        self.buttons = [self.woordToevoegButton, self.woordVerwijderButton, self.backButton] #
        self.SetSizer(boxje)

    def makeScherm(self):
        mainSizer = wx.BoxSizer()
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.Add(self.makeOptionBox(), 1, wx.CENTER)
        rightSizer.Add(self.makeWoordenBox(), 1, wx.CENTER)
        rightSizer.AddSpacer(30)
        rightSizer.Add(self.makeResolutionBox(), 1, wx.CENTER)
        rightSizer.AddSpacer(30)
        mainSizer.Add(leftSizer, 1, wx.LEFT)
        mainSizer.Add(rightSizer, 1, wx.RIGHT)
        return mainSizer

    def makeResolutionBox(self):
        resolutionSizer = wx.BoxSizer(wx.VERTICAL)
        self.choices = {"klein": (1280, 720),
                        "middel": (1366, 768),
                        "groot": (1920, 1080)
                        }
        self.resolutions = wx.RadioBox(self, -1, "Resolution:", choices=self.choices.keys(), majorDimension=1)
        resolutionSizer.Add(self.resolutions, 1, wx.LEFT)
        return resolutionSizer


    def makeWoordenBox(self):
        woordenSizer = wx.BoxSizer(wx.VERTICAL)
        self.woordToevoegButton = wx.Button(self, -1, "Woord toevoegen")
        self.woordVerwijderButton = wx.Button(self, -1, "Woord verwijderen")
        woordenSizer.AddSpacer(20)
        woordenSizer.Add(self.woordToevoegButton, 1, wx.LEFT)
        woordenSizer.AddSpacer(20)
        woordenSizer.Add(self.woordVerwijderButton, 1, wx.LEFT)
        return woordenSizer

    def makeOptionBox(self):
        optionBox = wx.BoxSizer(wx.VERTICAL)
        self.testmodeCheck = wx.CheckBox(self, -1, "Testmode")
        optionBox.AddSpacer(20)
        optionBox.AddSpacer(20)
        optionBox.Add(self.testmodeCheck, 1, wx.LEFT)
        return optionBox

    def makeBackButton(self):
        buttonSizer = wx.BoxSizer()
        self.backButton = wx.Button(self, -1, "Terug")
        buttonSizer.Add(self.backButton, 1, wx.LEFT)
        buttonSizer.Add(wx.Panel(self, -1), 10)
        return buttonSizer


    def center(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.CENTRE)
        return(hbox)

if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(600, 400),
                              style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX)
            boxje = wx.BoxSizer()
            boxje.Add(Schermpje(self, id), 1, wx.EXPAND | wx.ALL, 1)
            icon = wx.EmptyIcon()
            icon.CopyFromBitmap(wx.Bitmap("../Media/scrabble.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
            self.SetSizer(boxje)
            self.Centre()
            self.Show(True)


    app = wx.App()
    Naampje(None, -1, "Scrabble!")
    app.MainLoop()
