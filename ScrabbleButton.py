import wx
import string

class GameButton(wx.Button):
    def __init__(self, parent, id, location):
        wx.Button.__init__(self, parent, id, size=(60, 60))
        self.letter = ""
        self.tile_used = False
        self.woordMultiplier = 1
        self.letterMultiplier = 1
        self.score = {"a" : 1, "b" : 3, "c" : 3, "d" : 1, "e" : 1, "f" : 5,
                      "g" : 2, "h" : 2, "i" : 1, "j" : 4, "k" : 4, "l" : 2,
                      "m" : 3, "n" : 1, "o" : 1, "p" : 3, "q" : 10, "r" : 1,
                      "s" : 1, "t" : 1, "u" : 4, "v" : 4, "w" : 4, "x" : 8,
                      "y" : 8, "ij" : 4, "z" : 6, "" : 0}
        self.special = ""
        self.location = location
        self.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT,
                                       wx.FONTSTYLE_NORMAL,
                                       wx.FONTWEIGHT_NORMAL))

    def getLocation(self):
        return(self.location)

    def getLetterScore(self):
        if self.tile_used:
            return(self.score[self.letter])
        else:
            return(self.score[self.letter] * self.letterMultiplier)

    def getLetter(self):
        return(self.letter)

    def setLetter(self, sl_letter):
        if sl_letter in list(string.ascii_lowercase):
            if sl_letter != "q":
                label = ' %s\u208%s' % (sl_letter.upper(),
                                        self.score[sl_letter])
            else:
                label = 'Q\u2081\u2080'
            self.SetLabel(label.decode('unicode-escape'))
            """
            self.SetLabel(u'%s\u208%s' % (sl_letter.upper(),
                                          self.score[sl_letter]))
            """
            self.letter = sl_letter
            self.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT,
                                       wx.FONTSTYLE_NORMAL,
                                       wx.FONTWEIGHT_NORMAL))
            self.SetBackgroundColour('white')
        else:
            print("wrong letter given")

    def setTileUsed(self):
        self.tile_used = True

    def setTileUnused(self):
        self.tile_used = False

    def getTileStatus(self):
        return(self.tile_used)

    def setWoordMultiplier(self, sw_number):
        if type(sw_number) == int:
            self.woordMultiplier = sw_number

    def getWoordMultiplier(self):
        return(self.woordMultiplier)

    def setLetterMultiplier(self, sl_number):
        if type(sl_number) == int:
            self.letterMultiplier = sl_number

    def getLetterMultiplier(self):
        return(self.letterMultiplier)

    def resetButton(self):
        self.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT,
                                       wx.FONTSTYLE_NORMAL,
                                       wx.FONTWEIGHT_NORMAL))
        self.letter = ""
        self.tile_used = False
        if self.special == "dl":
            self.setDubbelLetter()
        elif self.special == "tl":
            self.setTripelLetter()
        elif self.special == "dw":
            self.setDubbelWoord()
        elif self.special == "tw":
            self.setTripelWoord()
        elif self.special == "mi":
            self.setMidden()
        else:
            self.woordMultiplier = 1
            self.letterMultiplier = 1
            self.SetLabel("")
            self.SetBackgroundColour(wx.NullColour)
        

    def setDubbelLetter(self):
        self.woordMultiplier = 1
        self.letterMultiplier = 2
        self.SetLabel("2L")
        self.SetBackgroundColour('light blue')
        self.special = "dl"

    def setTripelLetter(self):
        self.woordMultiplier = 1
        self.letterMultiplier = 3
        self.SetLabel("3L")
        self.SetBackgroundColour('blue')
        self.special = "tl"

    def setDubbelWoord(self):
        self.woordMultiplier = 2
        self.letterMultiplier = 1
        self.SetLabel("2W")
        self.SetBackgroundColour('pink')
        self.special = "dw"

    def setTripelWoord(self):
        self.woordMultiplier = 3
        self.letterMultiplier = 1
        self.SetLabel("3W")
        self.SetBackgroundColour('red')
        self.special = "tw"

    def setMidden(self):
        self.woordMultiplier = 2
        self.letterMultiplier = 1
        self.SetLabel(u'\u2605')
        self.SetBackgroundColour('pink')
        self.special = "mi"