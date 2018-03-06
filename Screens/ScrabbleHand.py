import wx
from ScrabbleButton import GameButton

class Hand(wx.BoxSizer):


    def __init__(self, window):
        wx.BoxSizer.__init__(self, wx.HORIZONTAL)
        self.window = window
        self.changeHand(['l', 'e', 't', 't', 'e', 'r', 's'])

    def changeHand(self, letters):
        self.fillHand(size=len(letters))
        self.letters = letters
        for i in range(len(self.letters)):
            self.GetChildren()[i].GetWindow().setLetter(self.letters[i])

    def fillHand(self, size=7):
        while len(self.GetChildren()) < size:
            self.Add(GameButton(self.window, 1, (0, 0)), 1, wx.CENTER)
        self.Layout()


    def removeLetter(self, letter):
        index = self.letters.index(letter)
        self.letters.pop(index)
        self.Hide(index)
        self.Remove(index)
        self.Layout()

    def addLetter(self, letter):
        button = GameButton(self.window, -1, (0, 0))
        button.setLetter(letter)
        self.Add(button)
        self.Layout()
