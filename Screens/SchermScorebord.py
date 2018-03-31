import wx
import wx.grid as gridlib

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        self.scoreboardLength = 7
        text = wx.StaticText(self, -1, "scorebord")
        text.SetFont(wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        boxje.Add(text, 1, wx.CENTER)
        boxje.Add(self.makeScreen(), 6)
        boxje.Add(self.makeBackButton(), 1, wx.ALIGN_BOTTOM, border=0)
        self.SetSizer(boxje)

    def makeScreen(self):
        mainBox = wx.BoxSizer()
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)
        leftSizer.AddSpacer(40)
        leftSizer.Add(self.makeGrid(), 1, wx.CENTER)
        rightSizer.AddSpacer(40)
        rightSizer.Add(self.makeRightButtonBox(), 1, wx.CENTER)
        mainBox.Add(leftSizer, 1, wx.LEFT)
        mainBox.Add(rightSizer, 1, wx.RIGHT)
        return mainBox

    def makeBackButton(self):
        buttonSizer = wx.BoxSizer()
        self.backButton = wx.Button(self, 1, "Terug")
        buttonSizer.Add(self.backButton, 1, wx.LEFT)
        buttonSizer.Add(wx.Panel(self, -1), 10)
        return buttonSizer

    def makeRightButtonBox(self):
        mainBox = wx.BoxSizer(wx.VERTICAL)
        self.csvButton = wx.Button(self, 2, "opslaan als csv")
        mainBox.AddSpacer(50)
        mainBox.Add(self.csvButton, 1, wx.CENTER)
        return mainBox

    def makeGrid(self):
        table = gridlib.Grid(self, -1)
        data = [
            ["naam", "score"],
            ["Sven", "10000"],
            ["Michael", "9001"],
            ["Steven", "6969"]
        ]
        self.scoreData = data[:self.scoreboardLength]
        table.CreateGrid(self.scoreboardLength, len(data[0]))
        header = data.pop(0)
        for i, x in enumerate(header):
            table.SetColLabelValue(i, x)
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                table.SetCellValue(i, j, item)
        return table


    def center(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.CENTRE)
        return(hbox)

if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(500, 350),
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
