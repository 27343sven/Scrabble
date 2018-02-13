import wx
from Screens.SchermSpelbord_oud import Schermpje as mainScherm
from Screens.PopupLetterScanner import Picker


class Schermpje2(wx.Frame):
    def __init__(self, parent, id, title):
        self.letters_in_beurt = 0
        self.current_beurt = 1
        self.score = 0
        self.beurten = {}
        self.tiles_this_turn = []
        wx.Frame.__init__(self, parent, id, title, size=(1500, 1000))
        self.boxje = wx.BoxSizer()
        self.scherm = mainScherm(self, -1)
        self.boxje.Add(self.scherm, 1, wx.EXPAND | wx.ALL, 1)
        self.bindStuff()
        #self.scherm.button_grid[0][1].Bind(wx.EVT_BUTTON, self.onButton)
        self.SetSizer(self.boxje)
        self.Centre()
        self.Show(True)

    def bindStuff(self):
        for x in self.scherm.button_grid:
            for y in x:
                y.Bind(wx.EVT_BUTTON, self.onButton)
        self.scherm.clearButton.Bind(wx.EVT_BUTTON, self.onClearButton)
        self.scherm.nextTurnButton.Bind(wx.EVT_BUTTON, self.onNextTurnButton)
        # self.scherm.backButton.Bind(wx.EVT_BUTTON, self.onBackButton)


    def onButton(self, event):
        current_object = event.GetEventObject()
        if not current_object.getTileStatus():
            if not (self.letters_in_beurt > 6 and
                    current_object.getLetter() == ""):
                test = Picker("Pick Letter")
                test.ShowModal()
                out = test.choice
                test.Destroy()
                if out != "":
                    if current_object.getLetter() == "":
                        self.letters_in_beurt += 1
                        self.tiles_this_turn.append(current_object.getLocation())
                    event.GetEventObject().setLetter(out)    
                else:
                    if current_object.getLetter() != "":
                        self.letters_in_beurt -= 1
                        self.tiles_this_turn.remove(current_object.getLocation())
                    current_object.resetButton()
        self.scherm.beurtLetters.SetLabel(str(self.letters_in_beurt))

    def onBackButton(self, event):
        if self.current_beurt != 1:
            negative_score = 0
            for x in self.beurten[self.current_beurt -1][1]:
                self.scherm.button_grid[x[0]][x[1]].resetButton()
            for x in self.beurten[self.current_beurt -1][0]:
                negative_score += x[1]
            for x in self.tiles_this_turn:
                self.scherm.button_grid[x[0]][x[1]].resetButton()
            del self.beurten[self.current_beurt -1]
            self.tiles_this_turn = []
            self.letters_in_beurt = 0
            self.score -= negative_score
            self.current_beurt -= 1
            self.scherm.beurtLetters.SetLabel("0")
            self.scherm.beurt.SetLabel(str(self.current_beurt) + " / 20")
            self.scherm.score.SetLabel(str(self.score))
            self.updateLog()
    
    def onClearButton(self, event):
        for x in self.tiles_this_turn:
            self.scherm.button_grid[x[0]][x[1]].resetButton()
        self.tiles_this_turn = []
        self.letters_in_beurt = 0
        self.scherm.beurtLetters.SetLabel("0")

    def onNextTurnButton(self, event):
        score_list = []
        if self.letters_in_beurt != 0:
            for y in range(len(self.scherm.button_grid)):
                for x in range(len(self.scherm.button_grid[y])):
                    if (self.scherm.button_grid[y][x].getLetter() != "" and
                        not y > 13 and not x > 13):
                        #horizontal
                        if self.scherm.button_grid[y][x + 1].getLetter() != "":
                            tb_woord, tb_score = self.horizontalWord([y, x])
                            if tb_woord != "Error":
                                score_list.append([tb_woord, tb_score])
                        if self.scherm.button_grid[y + 1][x].getLetter() != "":
                            tb_woord, tb_score = self.verticalWord([y, x])
                            if tb_woord != "Error":
                                score_list.append([tb_woord, tb_score])
            if self.letters_in_beurt > 6:
                score_list.append(["Bonus", 50])
            for x in self.tiles_this_turn:
                self.scherm.button_grid[x[0]][x[1]].setTileUsed()
            self.beurten[self.current_beurt] = [score_list,
                                                self.tiles_this_turn]
            for x in score_list:
                self.score += x[1]
            self.letters_in_beurt = 0
            self.current_beurt += 1
            self.tiles_this_turn = []
            self.scherm.beurtLetters.SetLabel("0")
            self.scherm.beurt.SetLabel(str(self.current_beurt) + " / 20")
            self.scherm.score.SetLabel(str(self.score))
            self.updateLog()

    def updateLog(self):
        output = ""
        beurten = self.beurten.keys()
        beurten.sort()
        if beurten != {}:
            for x in beurten:
                output += "===%s===\n" % (x)
                for y in self.beurten[x][0]:
                    output += "%s: %s\n" % (y[0], y[1])
                output += "\n"
        self.scherm.textbox.SetValue(output)
                        
    def horizontalWord(self, pos):
        woord = ""
        new = False
        woordMulti = 1
        woord_score = 0
        x = pos[1]
        y = pos[0]
        if self.scherm.button_grid[y][x - 1].getLetter() == "":
            while (not x > 13 and self.scherm.button_grid[y][x + 1].getLetter() != ""):
                woord_score += self.scherm.button_grid[y][x].getLetterScore()
                woordMulti *= self.scherm.button_grid[y][x].getWoordMultiplier()
                woord += self.scherm.button_grid[y][x].getLetter()
                if not self.scherm.button_grid[y][x].getTileStatus():
                    new = True
                x += 1
            woord_score += self.scherm.button_grid[y][x].getLetterScore()
            woordMulti *= self.scherm.button_grid[y][x].getWoordMultiplier()
            woord += self.scherm.button_grid[y][x].getLetter()
            if not self.scherm.button_grid[y][x].getTileStatus():
                new = True
            if new == True:
                score = woord_score * woordMulti
                return(woord, score)
        return("Error", 0)

    def verticalWord(self, pos):
        woord = ""
        new = False
        woordMulti = 1
        woord_score = 0
        x = pos[1]
        y = pos[0]
        if self.scherm.button_grid[y - 1][x].getLetter() == "":
            while (not y > 13 and self.scherm.button_grid[y + 1][x].getLetter() != ""):
                woord_score += self.scherm.button_grid[y][x].getLetterScore()
                woordMulti *= self.scherm.button_grid[y][x].getWoordMultiplier()
                woord += self.scherm.button_grid[y][x].getLetter()
                if not self.scherm.button_grid[y][x].getTileStatus():
                    new = True
                y += 1
            woord_score += self.scherm.button_grid[y][x].getLetterScore()
            woordMulti *= self.scherm.button_grid[y][x].getWoordMultiplier()
            woord += self.scherm.button_grid[y][x].getLetter()
            if not self.scherm.button_grid[y][x].getTileStatus():
                new = True
            if new == True:
                score = woord_score * woordMulti
                return(woord, score)
        return("Error", 0)

            


        
if __name__ == "__main__":
    app = wx.App()
    Schermpje2(None, -1, "button")
    app.MainLoop()
