import wx
import string as string_import
from ScrabbleButton import GameButton

class Picker(wx.Dialog):

    def __init__(self, title = 'myFrame'):
        wx.Dialog.__init__(self, None, -1, title=title, size=(500, 500))
        self.choice = ""
        self.buttonList, self.board = self.make_board()
        self.SetSizer(self.board)
        for x in self.buttonList:
            x.Bind(wx.EVT_BUTTON, self.onButton)

    def make_board(self):
        alpha = string_import.ascii_lowercase
        main_boxje = wx.BoxSizer(wx.VERTICAL)
        temp_boxje = wx.BoxSizer()
        main_list = []
        for x in range(len(alpha)):
            test = GameButton(self, -1, [int(x/6), x % 6])
            test.setLetter(alpha[x])
            temp_boxje.Add(test, 50, wx.EXPAND | wx.ALL, 1)
            main_list.append(test)
            if (x + 1) % 6 == 0:
                main_boxje.Add(temp_boxje, 50, wx.EXPAND | wx.ALL, 1)
                temp_boxje = wx.BoxSizer()
        emptyBox = GameButton(self, -1, [0, 0])
        temp_boxje.Add(emptyBox, 50, wx.EXPAND | wx.ALL, 1)
        main_list.append(emptyBox)
        temp_boxje.Add(wx.Panel(self, -1), 150, wx.EXPAND | wx.ALL, 1)
        main_boxje.Add(temp_boxje, 50, wx.EXPAND | wx.ALL, 1)
        
        return(main_list, main_boxje)

    def onButton(self, event):
        test = event.GetEventObject().getLetter()
        self.choice = test
        self.EndModal(wx.ID_OK)

        

        
if __name__ == "__main__":
    app = wx.App()
    test = Picker("What")
    test.ShowModal()
    print(test.choice)
    test.Destroy()
    app.MainLoop()
