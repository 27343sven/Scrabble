# screens
from Screens.SchermMenu import Schermpje as menuScherm
from Screens.SchermSettings import Schermpje as settingScherm
from Screens.SchermScorebord import Schermpje as highscoreScherm
from Screens.SchermWoordenToevoegen import Schermpje as woordenToevoegScherm
from Screens.SchermWoordenVerwijderen import Schermpje as woordenVerwijderScherm
from Screens.SchermPreGameOptions import Schermpje as spelSettingScherm
from Screens.SchermSpelbord import Schermpje as speelScherm
from Screens.SchermResultaat import Schermpje as resultaatScherm

# popups
from Screens.PopupLetterScanner import Picker

# classes
from Screens.ScrabbleGame import ScrableGame

import wx

class Schermpje2(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 600))
        self.schermen = {}
        self.initialiseerSchermen()
        self.game = ScrableGame()
        self.bindAll()
        self.setScherm('menu')

    def initialiseerSchermen(self):
        self.schermen = {'menu': [menuScherm(self, -1), (600, 400)],
                         'settings': [settingScherm(self, -1), (600, 400)],
                         'highscores': [highscoreScherm(self, -1), (500, 350)],
                         'woordenToevoeg': [woordenToevoegScherm(self, -1), (300, 186)],
                         'woordenVerwijder': [woordenVerwijderScherm(self, -1), (300, 186)],
                         'spelSettings': [spelSettingScherm(self, -1), (400, 400)],
                         'speelbord': [speelScherm(self, -1), (1500, 1000)],
                         'resultaat': [resultaatScherm(self, -1), (600, 400)]
                         }

    def setScherm(self, scherm):
        self.currentScherm = wx.BoxSizer()
        self.currentScherm.Add(self.schermen[scherm][0], 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizer(self.currentScherm)
        self.SetSize(self.schermen[scherm][1])
        for x in self.schermen:
            if x != scherm:
                self.schermen[x][0].Hide()  ##Hide alle andere schermen.
            else:
                self.schermen[x][0].Show()  ##Showt huidige scherm
                self.Layout()               ##Refresh windows anders wordt het heel raar.
        self.Centre()
        self.Show(True)

    def bindAll(self):
        self.bindMenu()
        self.bindHighscores()
        self.bindPreGame()
        self.bindSettings()
        self.bindToevoeg()
        self.bindVerwijder()
        self.bindSpeelScherm()
        self.bindPreGameOptions()

    def bindSpeelScherm(self):
        for row in self.schermen['speelbord'][0].button_grid:
            for button in row:
                button.Bind(wx.EVT_BUTTON, self.onScrabbleButton)
        self.schermen['speelbord'][0].clearButton.Bind(wx.EVT_BUTTON, self.onClearButton)
        self.schermen['speelbord'][0].nextTurnButton.Bind(wx.EVT_BUTTON, self.onNextTurnButton)

    def onScrabbleButton(self, event):
        current_object = event.GetEventObject()
        if not current_object.getTileStatus():
            test = Picker(self.game.getPlayerLetters(), clear=current_object.getLetter() != "")
            test.ShowModal()
            out = test.choice
            test.Destroy()
            if out not in [" ", ""]:
                if current_object.getLetter() != "":
                    self.clearLetter(current_object.getLetter())
                event.GetEventObject().setLetter(out)
                self.playLetter(out)
            elif out == " ":
                letter = current_object.resetButton()
                self.clearLetter(letter)

    def playLetter(self, letter):
        self.game.playLetter(letter)
        self.schermen['speelbord'][0].hand.removeLetter(letter)
        self.schermen['speelbord'][0].hand.Layout()
        self.game.letters_gespeeld += 1
        self.schermen['speelbord'][0].beurtLetters.SetLabel(str(self.game.letters_gespeeld))

    def clearLetter(self, letter):
        self.game.clearLetter(letter)
        self.schermen['speelbord'][0].hand.changeHand(self.game.getPlayerLetters())
        self.schermen['speelbord'][0].hand.Layout()
        self.game.letters_gespeeld -= 1
        self.schermen['speelbord'][0].beurtLetters.SetLabel(str(self.game.letters_gespeeld))

    def bindPreGameOptions(self):
        self.schermen['spelSettings'][0].spelenButton.Bind(wx.EVT_BUTTON, self.onPreGameOptionsSpelenButton)
        self.schermen['spelSettings'][0].backButton.Bind(wx.EVT_BUTTON, self.onPreGameOptionsTerugButton)

    def bindMenu(self):
        scherm = self.schermen['menu'][0]
        for button in scherm.buttons:
            button.Bind(wx.EVT_BUTTON, self.onMenuButton)

    def bindHighscores(self):
        scherm = self.schermen['highscores'][0]
        scherm.backButton.Bind(wx.EVT_BUTTON, self.onHighscoreButton)

    def bindPreGame(self):
        scherm = self.schermen['spelSettings'][0]
        for button in scherm.buttons:
            button.Bind(wx.EVT_BUTTON, self.onPreGameButton)

    def bindSettings(self):
        scherm = self.schermen['settings'][0]
        for button in scherm.buttons:
            button.Bind(wx.EVT_BUTTON, self.onSettingsButton)

    def bindToevoeg(self):
        scherm = self.schermen['woordenToevoeg'][0]
        for button in scherm.buttons:
            button.Bind(wx.EVT_BUTTON, self.onToevoegButton)

    def bindVerwijder(self):
        scherm = self.schermen['woordenVerwijder'][0]
        for button in scherm.buttons:
            button.Bind(wx.EVT_BUTTON, self.onVerwijderButton)

    def onNextTurnButton(self, event):
        if self.game.letters_gespeeld == 0:
            dlg = wx.MessageDialog(self, "Please place a word before going to the next turn. If you cannot place a word you can exchange your letters.", "No Letters Played",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if not self.checkIfNewLettersInLine():
            dlg = wx.MessageDialog(self,
                                    "All letters must be placed in one line.",
                                    "Letters not in line",
                                    wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if self.checkLosseLetters():
            dlg = wx.MessageDialog(self,
                                   "There are still lone letters on the board.",
                                   "Lose letters",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        score_list, validTrun, statusList, position_list = [], True, [], []
        for y in range(len(self.schermen['speelbord'][0].button_grid)):
            for x in range(len(self.schermen['speelbord'][0].button_grid[y])):
                if self.schermen['speelbord'][0].button_grid[y][x].getLetter() != "":
                    if not x > 13 and self.getNextTileLetter((x, y), True) != "":
                        tb_status, tb_woord, tb_score, word_pos = self.checkForWoord((x, y), True)
                        statusList.append(tb_status)
                        if tb_status == "ok":
                            position_list.append(word_pos)
                            score_list.append([tb_woord, tb_score])
                        if self.game.isFirstTurn():
                            if tb_status == "notInMiddle":
                                position_list.append(word_pos)
                        else:
                            if tb_status == "notConnected":
                                position_list.append(word_pos)
                    if not y > 13 and self.getNextTileLetter((x, y), False) != "":
                        tb_status, tb_woord, tb_score, word_pos = self.checkForWoord((x, y), False)
                        statusList.append(tb_status)
                        if tb_status == "ok":
                            position_list.append(word_pos)
                            score_list.append([tb_woord, tb_score])
                        if self.game.isFirstTurn():
                            if tb_status == "notInMiddle":
                                position_list.append(word_pos)
                        else:
                            if tb_status == "notConnected":
                                position_list.append(word_pos)
        if len(position_list) != len(set(position_list)):
            # als er twee geldige woorden op dezelfde lijn worden gespeeld
            dlg = wx.MessageDialog(self, "You can only place one word.", "Multiple words",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        elif "notConnected" in statusList:
            # als er woorden niet aan oude letters liggen na de eerste beurt
            dlg = wx.MessageDialog(self, "New words must connect to old ones.", "Word not connected",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        elif "notInMiddle" in statusList:
            # als de letters niet in het midden liggen tijdens de eerste beurt
            dlg = wx.MessageDialog(self, "Must place first word in middle.", "Word not in middle", wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        elif score_list:
            self.game.addScore(score_list)
            self.lockLetters()
            self.game.nextTurn()
            self.refreshInfo()

    def lockLetters(self):
        for y in range(len(self.schermen['speelbord'][0].button_grid)):
            for x in range(len(self.schermen['speelbord'][0].button_grid[y])):
                button = self.schermen['speelbord'][0].button_grid[y][x]
                if button.getLetter() != "" and not button.getTileStatus():
                    button.setTileUsed()

    def checkIfNewLettersInLine(self):
        all_x, all_y = [], []
        for y in range(len(self.schermen['speelbord'][0].button_grid)):
            for x in range(len(self.schermen['speelbord'][0].button_grid[y])):
                if self.schermen['speelbord'][0].button_grid[y][x].getLetter() != "" \
                        and not self.schermen['speelbord'][0].button_grid[y][x].getTileStatus():
                    all_x.append(x)
                    all_y.append(y)
        if len(set(all_x)) == 1 or len(set(all_y)) == 1:
            return True
        else:
            return False

    def checkLosseLetters(self):
        for y in range(len(self.schermen['speelbord'][0].button_grid)):
            for x in range(len(self.schermen['speelbord'][0].button_grid[y])):
                if self.schermen['speelbord'][0].button_grid[y][x].getLetter() != "":
                    isConnected = False
                    for orientation in (True, False):
                        if self.getNextTileLetter((x, y), orientation) != "" or self.getPreviousTileLetter((x, y), orientation) != "":
                            isConnected = True
                    if not isConnected:
                        return True
        return False


    def getNextTileLetter(self, pos, horizontal):
        x, y = pos[0], pos[1]
        if horizontal and not x > 13:
            return self.schermen['speelbord'][0].button_grid[y][x + 1].getLetter()
        elif not y > 13:
            return self.schermen['speelbord'][0].button_grid[y + 1][x].getLetter()
        return None

    def getNextTileStatus(self, pos, horizontal):
        x, y = pos[0], pos[1]
        if horizontal and not x > 13:
            return self.schermen['speelbord'][0].button_grid[y][x + 1].getTileStatus()
        elif not y > 13:
            return self.schermen['speelbord'][0].button_grid[y + 1][x].getTileStatus()
        return False

    def getPreviousTileLetter(self, pos, horizontal):
        x, y = pos[0], pos[1]
        if horizontal and x > 0:
            return self.schermen['speelbord'][0].button_grid[y][x - 1].getLetter()
        elif y > 0:
            return self.schermen['speelbord'][0].button_grid[y - 1][x].getLetter()
        return None

    def getPreviousTileStatus(self, pos, horizontal):
        x, y = pos[0], pos[1]
        if horizontal and x > 0:
            return self.schermen['speelbord'][0].button_grid[y][x - 1].getTileStatus()
        elif y > 0:
            return self.schermen['speelbord'][0].button_grid[y - 1][x].getTileStatus()
        return False

    def getAllTileLetters(self):
        for y in range(len(self.schermen['speelbord'][0].button_grid)):
            for x in range(len(self.schermen['speelbord'][0].button_grid[y])):
                letter = self.schermen['speelbord'][0].button_grid[y][x].getLetter()
                if letter:
                    print("{}|{}|{}".format(x, y, letter))

    def findWoord(self, pos, horizontal):
        woord, new, woordMulti, woord_score, x, y, middle, connected = "", False, 1, 0, pos[0], pos[1], False, False
        while not y > 13 and not x > 13:
            if x == 7 and y == 7:
                middle = True
            woord_score += self.schermen['speelbord'][0].button_grid[y][x].getLetterScore()
            woordMulti *= self.schermen['speelbord'][0].button_grid[y][x].getWoordMultiplier()
            woord += self.schermen['speelbord'][0].button_grid[y][x].getLetter()
            if self.schermen['speelbord'][0].button_grid[y][x].getTileStatus():
                connected = True
            else:
                if self.getPreviousTileStatus((x, y), not horizontal) or self.getNextTileStatus((x, y), not horizontal):
                    # als het gespeelde woord uit alleen maar nieuwe letters bestaat maar wel aan eerder
                    # gespeelde letters ligt
                    print("yay")
                    connected = True
                new = True
            if self.getNextTileLetter((x, y), horizontal) == "":
                break
            if horizontal:
                x += 1
            else:
                y += 1
        return new, woord, woordMulti, woord_score, middle, connected

    def checkForWoord(self, pos, horizontal):
        if self.getPreviousTileLetter(pos, horizontal) == "":
            new, woord, woordMulti, woord_score, middle, connected = self.findWoord(pos, horizontal)
            if new:
                if self.game.isFirstTurn() and not middle:
                    return "notInMiddle", "Error", 0, (horizontal, pos[1] if horizontal else pos[0])
                if not self.game.isFirstTurn() and not connected:
                    return "notConnected", "Error", 0, (horizontal, pos[1] if horizontal else pos[0])
                score = woord_score * woordMulti
                return "ok", woord, score, (horizontal, pos[1] if horizontal else pos[0])
        return "notNew", "Error", 0, (horizontal, pos[1] if horizontal else pos[0])

    def refreshInfo(self):
        self.schermen['speelbord'][0].speler.SetLabel(self.game.getCurrentPlayer())
        self.schermen['speelbord'][0].score.SetLabel(str(self.game.getCurrentScore()))
        self.schermen['speelbord'][0].beurtLetters.SetLabel(str(self.game.getAantalLettersGespeeld()))
        self.schermen['speelbord'][0].hand.changeHand(self.game.getPlayerLetters())
        self.schermen['speelbord'][0].textbox.SetValue("\n".join(self.game.getLog()))
        self.setScherm('speelbord')

    def onClearButton(self, event):
        for row in self.schermen['speelbord'][0].button_grid:
            for button in row:
                if button.getLetter() != "" and not button.getTileStatus():
                    letter = button.resetButton()
                    self.clearLetter(letter)

    def onPreGameOptionsSpelenButton(self, event):
        scherm = self.schermen['spelSettings'][0]
        namen = []
        for x in range(int(scherm.playerOption.GetStringSelection())):
            namen.append(scherm.textCtrlDict['textCtrl{}'.format(x + 1)].GetValue())
        self.game.setPlayers(namen)
        self.schermen['speelbord'][0].speler.SetLabel(self.game.getCurrentPlayer())
        self.schermen['speelbord'][0].hand.changeHand(self.game.getPlayerLetters())
        self.setScherm('speelbord')

    def onPreGameOptionsTerugButton(self, event):
        scherm = self.schermen['spelSettings'][0]
        for x in range(int(scherm.playerOption.GetStringSelection())):
            scherm.textCtrlDict['textCtrl{}'.format(x + 1)].Clear()
        scherm.playerOption.SetSelection(0)
        scherm.onRadioBox(None)
        self.setScherm('menu')

    def onMenuButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('spelSettings')
        elif object.GetId() == 2:
            self.setScherm('settings')
        elif object.GetId() == 3:
            self.setScherm('highscores')
        elif object.GetId() == 4:
            self.Close()

    def onHighscoreButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('menu')
            
    def onPreGameButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == -31943:    ##idk don't question it...
            self.setScherm('menu')
        elif object.GetId() == -31942:
            self.setScherm('speelbord')

    def onSettingsButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == -31980:
            self.setScherm('menu')
        elif object.GetId() == -31987:
            self.setScherm('woordenToevoeg')     ##Uuh.. kreeg het niet als popup.
        elif object.GetId() == -31986:
            self.setScherm('woordenVerwijder')

    def onToevoegButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == -31966:
            self.setScherm('settings')
        if object.GetId() == -31967:
            print("Toevoeg woord: " +
                self.schermen['woordenToevoeg'][0].textBox.GetValue().lower())

    def onVerwijderButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == -31960:
            self.setScherm('settings')
        if object.GetId() == -31961:    
            print("Verwijder woord: " +
                  self.schermen['woordenVerwijder'][0].textBox.GetValue().lower())

if __name__ == "__main__":
    app = wx.App()
    Schermpje2(None, -1, "Scrabble!")
    app.MainLoop()

