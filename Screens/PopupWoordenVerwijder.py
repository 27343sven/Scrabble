import wx
import string as string_import
from ScrabbleButton import GameButton


class Picker(wx.Dialog):

    def __init__(self, title='myFrame'):
        wx.Dialog.__init__(self, None, -1, title=title, size=(300, 158))
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Woord verwijderen")
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
        self.toevoegButton = wx.Button(self, -1, "Verwijderen")  # <--kek
        self.terugButton = wx.Button(self, -1, "Terug")
        self.buttons = [self.toevoegButton, self.terugButton]  #
        buttonBox.Add(self.terugButton, 1, wx.LEFT)
        buttonBox.Add(wx.Panel(self, -1), 2)
        buttonBox.Add(self.toevoegButton, 1, wx.RIGHT)
        return buttonBox

    def onButton(self, event):
        test = event.GetEventObject().getLetter()
        self.choice = test
        self.EndModal(wx.ID_OK)

if __name__ == '__main__':
    app = wx.App()
    test = Picker("What")
    test.ShowModal()
    print(test.choice)
    test.Destroy()
    app.MainLoop()