import wx
from ScrabbleButton import GameButton

class Schermpje(wx.Panel):
    
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer()
        self.button_grid, self.board = self.make_board()
        self.textbox = wx.TextCtrl(self, value="",
                                   style=wx.TE_MULTILINE | wx.TE_READONLY)
        boxje.Add(self.left_side(), 200, wx.EXPAND | wx.ALL)
        boxje.Add(self.center(self.board), 770, wx.EXPAND | wx.ALL)
        boxje.Add(self.textbox, 200, wx.EXPAND | wx.ALL)
        self.SetSizer(boxje)

    def left_side(self):
        button_boxje = wx.BoxSizer(wx.VERTICAL)
        button_boxje2 = wx.BoxSizer(wx.VERTICAL)
        # button_boxje3 = wx.BoxSizer(wx.VERTICAL)
        main_boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Aantal letters deze beurt: ")
        text2 = wx.StaticText(self, -1, "Score:")
        text3 = wx.StaticText(self, -1, "Beurt:")
        text4 = wx.StaticText(self, -1, "Speler: Sven")
        self.clearButton = wx.Button(self, -1, "Clear")
        # self.backButton = wx.Button(self, -1, "Back")
        self.nextTurnButton = wx.Button(self, -1, "Volgende Beurt")
        self.wisselButton = wx.Button(self, -1, "wissel in")
        self.beurtLetters = wx.StaticText(self, -1, "0")
        self.score = wx.StaticText(self, -1, "0")
        self.beurt = wx.StaticText(self, -1, "1")

        button_boxje.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)
        button_boxje.Add(self.nextTurnButton, 2, wx.EXPAND | wx.ALL)
        button_boxje.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)

        button_boxje2.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)
        button_boxje2.Add(self.clearButton, 2, wx.EXPAND | wx.ALL)
        button_boxje2.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)

        button_boxje.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)
        button_boxje.Add(self.wisselButton, 2, wx.EXPAND | wx.ALL)
        button_boxje.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)

        # button_boxje3.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)
        # button_boxje3.Add(self.backButton, 2, wx.EXPAND | wx.ALL)
        # button_boxje3.Add(wx.Panel(self, -1), 1, wx.EXPAND | wx.ALL)

        beurtSizer = wx.BoxSizer()
        beurtSizer.Add(text3, 1)
        beurtSizer.AddSpacer(10)
        beurtSizer.Add(self.beurt, 5)
        main_boxje.Add(beurtSizer, 20, wx.EXPAND | wx.ALL | wx.LEFT)
        # main_boxje.Add(self.center(self.beurt),
        #                50, wx.EXPAND | wx.ALL)

        blerg = wx.BoxSizer()
        blerg.Add(text4, 1)
        blerg.AddSpacer(10)
        blerg.Add(self.beurt, 5)
        main_boxje.Add(beurtSizer, 20, wx.EXPAND | wx.ALL | wx.LEFT)

        aantalLettersSizer = wx.BoxSizer()
        aantalLettersSizer.Add(text, 1)
        aantalLettersSizer.Add(self.beurtLetters, 1)
        main_boxje.Add(aantalLettersSizer, 20, wx.EXPAND | wx.ALL | wx.LEFT)
        # main_boxje.Add(self.center(self.beurtLetters),
        #                50, wx.EXPAND | wx.ALL)

        scoreSizer = wx.BoxSizer()
        scoreSizer.Add(text2, 1)
        scoreSizer.Add(self.score, 1)
        main_boxje.Add(scoreSizer, 20, wx.EXPAND | wx.ALL)
        # main_boxje.Add(self.center(self.score),
        #                50, wx.EXPAND | wx.ALL)

        letterText = wx.StaticText(self, -1, "Letters:")
        letterSizer1 = wx.BoxSizer()
        letterSizer2 = wx.BoxSizer()
        letters = ['h', 'a', 'l', 'l', 'o', 't', 'z']
        for x in letters[:4]:
            button = GameButton(self, -1, [-1, -1])
            button.setLetter(x)
            letterSizer1.Add(button)
        for x in letters[4:]:
            button = GameButton(self, -1, [-1, -1])
            button.setLetter(x)
            letterSizer2.Add(button)
        main_boxje.Add(wx.Panel(self, -1), 50, wx.EXPAND | wx.ALL)
        main_boxje.Add(letterText, 20)
        main_boxje.Add(letterSizer1, 20)
        main_boxje.Add(letterSizer2, 20)
        main_boxje.Add(wx.Panel(self, -1), 50, wx.EXPAND | wx.ALL)
        main_boxje.Add(button_boxje2, 50, wx.EXPAND | wx.ALL)
        # main_boxje.Add(button_boxje3, 50, wx.EXPAND | wx.ALL)
        main_boxje.Add(button_boxje, 50, wx.EXPAND | wx.ALL)

        return(main_boxje)

    def center(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.CENTRE)
        return(hbox)
    
    def make_board(self):
        main_boxje = wx.BoxSizer(wx.VERTICAL)
        main_list = []
        for x in range(15):
            temp_boxje = wx.BoxSizer()
            temp_list = []
            for y in range(15):
                test = GameButton(self, -1, [x, y])
                temp_boxje.Add(test, 1, wx.EXPAND | wx.ALL)
                temp_list.append(test)
            main_boxje.Add(temp_boxje, 1, wx.EXPAND | wx.ALL)
            main_list.append(temp_list)
        self.set_tiles(main_list)
        return(main_list, main_boxje)

    def set_tiles(self, board):
        #tripel woord waarden
        board[0][0].setTripelWoord()
        board[0][7].setTripelWoord()
        board[0][14].setTripelWoord()
        board[7][0].setTripelWoord()
        board[7][14].setTripelWoord()
        board[14][0].setTripelWoord()
        board[14][7].setTripelWoord()
        board[14][14].setTripelWoord()
        
        #dubbel woord waarden
        board[1][1].setDubbelWoord()
        board[2][2].setDubbelWoord()
        board[3][3].setDubbelWoord()
        board[4][4].setDubbelWoord()
        board[13][13].setDubbelWoord()
        board[12][12].setDubbelWoord()
        board[11][11].setDubbelWoord()
        board[10][10].setDubbelWoord()
        board[1][13].setDubbelWoord()
        board[2][12].setDubbelWoord()
        board[3][11].setDubbelWoord()
        board[4][10].setDubbelWoord()
        board[13][1].setDubbelWoord()
        board[12][2].setDubbelWoord()
        board[11][3].setDubbelWoord()
        board[10][4].setDubbelWoord()

        #tripel letter waarden
        board[1][5].setTripelLetter()
        board[1][9].setTripelLetter()
        board[5][1].setTripelLetter()
        board[5][5].setTripelLetter()
        board[5][9].setTripelLetter()
        board[5][13].setTripelLetter()
        board[9][1].setTripelLetter()
        board[9][5].setTripelLetter()
        board[9][9].setTripelLetter()
        board[9][13].setTripelLetter()
        board[13][5].setTripelLetter()
        board[13][9].setTripelLetter()

        #dubbel letter waarden
        board[0][3].setDubbelLetter()
        board[0][11].setDubbelLetter()
        board[3][0].setDubbelLetter()
        board[11][0].setDubbelLetter()
        board[14][3].setDubbelLetter()
        board[14][11].setDubbelLetter()
        board[3][14].setDubbelLetter()
        board[11][14].setDubbelLetter()
        board[2][6].setDubbelLetter()
        board[3][7].setDubbelLetter()
        board[2][8].setDubbelLetter()
        board[6][2].setDubbelLetter()
        board[7][3].setDubbelLetter()
        board[8][2].setDubbelLetter()
        board[12][6].setDubbelLetter()
        board[11][7].setDubbelLetter()
        board[12][8].setDubbelLetter()
        board[6][12].setDubbelLetter()
        board[7][11].setDubbelLetter()
        board[8][12].setDubbelLetter()
        board[6][6].setDubbelLetter()
        board[8][6].setDubbelLetter()
        board[6][8].setDubbelLetter()
        board[8][8].setDubbelLetter()
        #maak het midden
        board[7][7].setMidden()
        return(board)

if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(1500, 930),
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
