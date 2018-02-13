import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Woord toevoegen")
        text.SetFont(wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        self.textBox = wx.TextCtrl(self, -1)
        boxje.Add(text, 0, wx.CENTER)
        boxje.AddSpacer(30)
        boxje.Add(self.textBox, 0, wx.CENTER)
        boxje.AddSpacer(40)
        boxje.Add(self.makeButtonBox(), 0, wx.BOTTOM)
        self.SetSizer(boxje)

    def makeButtonBox(self):
        buttonBox = wx.BoxSizer()
        self.toevoegButton = wx.Button(self, -1, "Toevoegen")
        self.terugButton = wx.Button(self, -1, "Terug")
        self.buttons = [self.toevoegButton, self.terugButton] #
        buttonBox.Add(self.terugButton, 1, wx.LEFT)
        buttonBox.Add(wx.Panel(self, -1), 2)
        buttonBox.Add(self.toevoegButton, 1, wx.RIGHT)
        return buttonBox

if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(300, 181),
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
