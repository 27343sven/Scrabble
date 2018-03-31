import wx
from ScrabbleButton import GameButton
from ScrabbleHand import Hand


class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer()
        self.button_grid, self.board = self.make_board()
        self.textbox = wx.TextCtrl(self, value="",
                                   style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.textbox.SetFont(wx.Font(10, wx.MODERN, wx.NORMAL, wx.NORMAL, False))
        boxje.Add(self.left_side2(), 200, wx.EXPAND | wx.ALL)
        boxje.Add(self.center(self.board), 770, wx.EXPAND | wx.ALL)
        boxje.Add(self.textbox, 200, wx.EXPAND | wx.ALL)
        self.SetSizer(boxje)


    def left_side2(self):
        # declaring buttons
        self.clearButton = wx.Button(self, 1, "Clear")
        self.nextTurnButton = wx.Button(self, 2, "Volgende Beurt")
        self.wisselButton = wx.Button(self, 3, "wissel in")

        # voeg de hele linker kant samen
        left_box = wx.BoxSizer(wx.VERTICAL)
        left_box.AddMany([(self.makeInfoBox(), 6, wx.EXPAND | wx.ALL),
                          (wx.Panel(self, -1), 40, wx.EXPAND | wx.ALL),
                          (self.clearButton, 3, wx.EXPAND | wx.ALL),
                          (wx.Panel(self, -1), 2, wx.EXPAND | wx.ALL),
                          (self.nextTurnButton, 3, wx.EXPAND | wx.ALL),
                          (wx.Panel(self, -1), 2, wx.EXPAND | wx.ALL),
                          (self.wisselButton, 3, wx.EXPAND | wx.ALL)])
        return left_box

    def makeInfoBox(self):
        # maakt het boxje met het aantal beurten en
        info_box = wx.BoxSizer(wx.VERTICAL)
        letter_box = wx.BoxSizer()
        score_box = wx.BoxSizer()
        speler_box = wx.BoxSizer()

        self.speler = wx.StaticText(self, -1, "Henk")
        self.beurtLetters = wx.StaticText(self, -1, "0")
        self.score = wx.StaticText(self, -1, "0")
        spelerSupport = wx.StaticText(self, -1, "Speler: ")
        beurtLettersSupport = wx.StaticText(self, -1, "aantal letters deze beurt: ")
        scoreSupport = wx.StaticText(self, -1, "Score: ")

        speler_box.AddMany([(spelerSupport, 1, wx.LEFT),
                            (self.speler, 1, wx.LEFT)])
        letter_box.AddMany([(beurtLettersSupport, 1, wx.LEFT),
                            (self.beurtLetters, 1, wx.LEFT)])
        score_box.AddMany([(scoreSupport, 1, wx.LEFT),
                           (self.score, 1, wx.LEFT)])
        info_box.AddMany([(speler_box, 1), (wx.Panel(self, -1), 2, wx.EXPAND | wx.ALL),
                          (letter_box, 1), (wx.Panel(self, -1), 2, wx.EXPAND | wx.ALL),
                          (score_box, 1)])

        return info_box

    def center(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.CENTRE)
        return (hbox)

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
        self.hand = Hand(self)
        main_boxje.Add(wx.Panel(self, -1), 1)
        main_boxje.Add(self.hand, 0, wx.CENTER)
        return (main_list, main_boxje)

    def set_tiles(self, board):
        trippel_woord = [(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0), (14, 7), (14, 14)]
        dubbel_woord = [(1, 1), (2, 2), (3, 3), (4, 4), (13, 13), (12, 12), (11, 11), (10, 10),
                        (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4)]
        trippel_letter = [(1, 5), (1, 9), (5, 1), (5, 5), (5, 9), (5, 13), (9, 1), (9, 5), (9, 9),
                         (9, 13), (13, 5), (13, 9)]
        dubbel_letter = [(0, 3), (0, 11), (3, 0), (11, 0), (14, 3), (14, 11), (3, 14), (11, 14),
                         (2, 6), (3, 7), (2, 8), (6, 2), (7, 3), (8, 2), (12, 6), (11, 7), (12, 8),
                         (6, 12), (7, 11), (8, 12), (6, 6), (8, 6), (6, 8), (8, 8)]
        for (x, y) in trippel_woord:
            board[x][y].setTripelWoord()
        for (x, y) in dubbel_woord:
            board[x][y].setDubbelWoord()
        for (x, y) in trippel_letter:
            board[x][y].setTripelLetter()
        for (x, y) in dubbel_letter:
            board[x][y].setDubbelLetter()
        # maak het midden
        board[7][7].setMidden()
        return (board)


if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(1500, 1000),
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
