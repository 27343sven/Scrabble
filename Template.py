import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "LORUM IPSUM")
        text.SetFont(wx.Font(50, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        boxje.Add(text, 1, wx.CENTER)
        self.SetSizer(boxje)

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
            icon = wx.Icon()
            icon.CopyFromBitmap(wx.Bitmap("scrabble.ico", wx.BITMAP_TYPE_ANY))
            self.SetIcon(icon)
            self.SetSizer(boxje)
            self.Centre()
            self.Show(True)


    app = wx.App()
    Naampje(None, -1, "Scrabble!")
    app.MainLoop()