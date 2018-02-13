import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Resultaten:")
        text.SetFont(wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        text2 = wx.StaticText(self, -1, "Winnaar: Steven")
        text2.SetFont(wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        text3 = wx.StaticText(self, -1, "Punten: 9001")
        text3.SetFont(wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        boxje.Add(text, 2, wx.CENTER)
        boxje.Add(text2, 1, wx.CENTER)
        boxje.Add(text3, 1, wx.CENTER)
        boxje.Add(self.makeBackButton())
        self.SetSizer(boxje)

    def makeBackButton(self):
        buttonSizer = wx.BoxSizer()
        self.backButton = wx.Button(self, 1, "Terug")
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
            icon.CopyFromBitmap(wx.Bitmap("scrabble.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
            self.SetSizer(boxje)
            self.Centre()
            self.Show(True)


    app = wx.App()
    Naampje(None, -1, "Scrabble!")
    app.MainLoop()