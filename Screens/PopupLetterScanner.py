import wx
import string as string_import
from ScrabbleButton import GameButton


class Picker(wx.Dialog):

    def __init__(self, letters, clear=False, title='Scrabble! - Pick a letter'):
        wx.Dialog.__init__(self, None, -1, title=title, size=(450, 150))
        self.choice = ""
        self.clear = clear
        self.letters = letters
        self.buttonList, self.board = self.make_board()
        self.SetSizer(self.board)
        for x in self.buttonList:
            x.Bind(wx.EVT_BUTTON, self.onButton)

    def make_board(self):
        self.clearButton = wx.Button(self, -1, "Clear")
        if not self.clear:
            self.clearButton.Hide()
        self.clearButton.Bind(wx.EVT_BUTTON, self.onClearButton)
        main_boxje = wx.BoxSizer(wx.VERTICAL)
        temp_boxje = wx.BoxSizer()
        main_list = []
        for x in range(len(self.letters)):
            test = GameButton(self, -1, [int(x / 7), x % 7])
            test.setLetter(self.letters[x])
            temp_boxje.Add(test, 50, 1)
            main_list.append(test)
        main_boxje.Add(temp_boxje, 50, 1)
        main_boxje.AddSpacer(20)
        main_boxje.Add(self.clearButton, 1, 1)

        return (main_list, main_boxje)

    def onButton(self, event):
        test = event.GetEventObject().getLetter()
        self.choice = test
        self.EndModal(wx.ID_OK)

    def onClearButton(self, event):
        self.choice = " "
        self.EndModal(wx.ID_OK)


if __name__ == "__main__":
    app = wx.App()
    test = Picker(['l', 'e', 't', 't', 'e', 'r', 's'])
    test.ShowModal()
    print(test.choice)
    test.Destroy()
    app.MainLoop()
