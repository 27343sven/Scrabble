import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id, SCORE=['Steven', 9001]):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        self.text = wx.StaticText(self, -1, "Resultaten:")
        self.text.SetFont(wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.text2 = wx.StaticText(self, -1, "Winnaar: " + SCORE[0])
        self.text2.SetFont(wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        self.text3 = wx.StaticText(self, -1, "Punten: " + str(SCORE[1]))
        self.text3.SetFont(wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        boxje.Add(self.text, 2, wx.CENTER)
        boxje.Add(self.text2, 1, wx.CENTER)
        boxje.Add(self.text3, 1, wx.CENTER)
        boxje.Add(self.makeBackButton())
        self.SetSizer(boxje)

    def makeBackButton(self):
        buttonSizer = wx.BoxSizer()
        self.backButton = wx.Button(self, 1, "Terug")
        self.scoreBoardButton = wx.Button(self, 2, "Scoreboard")
        buttonSizer.Add(self.backButton, 1, wx.LEFT)
        buttonSizer.Add(wx.Panel(self, -1), 10)
        buttonSizer.Add(self.scoreBoardButton, 1, wx.RIGHT)
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
