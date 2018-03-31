import wx
import string as string_import
from ScrabbleToggleButton import GameButton


class Picker(wx.Dialog):
    def __init__(self, letters=('d', 'e', 'f', 'a', 'u', 'l', 't'), icon_path="../Media/", icon_file="scrabble.ico"):
        wx.Dialog.__init__(self, None, -1, title="Scrabble!", size=(500, 300))
        self.weggooiLetters = []
        self.buttonList, self.board = self.make_board(letters)
        self.SetSizer(self.board)
        for x in self.buttonList:
            x.Bind(wx.EVT_TOGGLEBUTTON, self.onButton)
        self.backButton.Bind(wx.EVT_BUTTON, self.onBackButton)
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap("{}{}".format(icon_path, icon_file), wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)

    def make_board(self, letters):
        main_boxje = wx.BoxSizer(wx.VERTICAL)
        letterbox = wx.BoxSizer()
        main_list = []
        text = wx.StaticText(self, -1, "Kies letters om weg te gooien:")
        text.SetFont(wx.Font(20, wx.ROMAN, wx.NORMAL, wx.NORMAL))
        main_boxje.Add(text, 1, wx.CENTER)
        for x in range(len(letters)):
            test = GameButton(self, -1, [int(x / 6), x % 6])
            test.setLetter(letters[x])
            letterbox.Add(test, 50, 1, wx.CENTER)
            main_list.append(test)
        main_boxje.AddSpacer(30)
        main_boxje.Add(letterbox, 1, wx.CENTER)
        main_boxje.AddSpacer(30)
        self.backButton = wx.Button(self, -1, "Wissel")
        self.annuleerButton = wx.Button(self, -1, "Annuleer")

        main_boxje.Add(self.backButton, 1, wx.CENTER)
        main_boxje.Add(self.annuleerButton, 1, wx.CENTER)
        return (main_list, main_boxje)

    def onButton(self, event):
        test = event.GetEventObject()
        if test.GetValue():
            test.SetBackgroundColour('grey')
        else:
            test.SetBackgroundColour('white')

    def onBackButton(self, event):
        for i, x in enumerate(self.buttonList):
            if x.GetValue():
                self.weggooiLetters.append(i)
        if len(self.weggooiLetters) > 0:
            self.EndModal(wx.ID_OK)
        else:
            dlg = wx.MessageDialog(self, "Gooi tenminste een letter weg", "Gooi een letter weg",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()



if __name__ == "__main__":
    hand = ["l",  "e", "t", "t", "e", "r", "s"]
    app = wx.App()
    test = Picker(hand)
    test.ShowModal()
    print(test.weggooiLetters)
    for i, x in enumerate(test.weggooiLetters):
        hand.pop(x-i)
    print(hand)
    test.Destroy()
    app.MainLoop()
