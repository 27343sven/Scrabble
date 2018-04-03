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
from Screens.LetterInwisselScanner import Picker as InwisselPopup

# classes
from Screens.ScrabbleGame import ScrableGame
from Screens.WordCheck import WordCheck

import wx
import csv

class Schermpje2(wx.Frame):
    HIGHSCORES = []
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 600))
        self.schermen = {}
        self.initialiseerSchermen()
        self.game = ScrableGame()
        self.woordenboek = WordCheck(path="./Media/")
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
        self.schermen['speelbord'][0].wisselButton.Bind(wx.EVT_BUTTON, self.onWisselButton)

        #Test button
        self.schermen['speelbord'][0].endButton.Bind(wx.EVT_BUTTON, self.onEndButton)


    #Test button
    def onEndButton(self, event):
        # Get current scores and put it in a list
        self.tempVar = self.game.getPlayerInfo()
        currentScore = []
        for i in self.tempVar:
            currentScore.append([str(i), self.tempVar[i]['score']])
        
        # Appends list of current scores to existing highscores
        for i in currentScore:
            self.HIGHSCORES.append(i)

        # Sort the list of scores from high to low
        currentScore.sort(key=lambda x: x[1], reverse=True)
        # Renew highscoreScreen to update scoreboard
        self.schermen['highscores'] = [highscoreScherm(self, -1, self.HIGHSCORES), (500, 350)]
        # Rebind buttons
        self.bindHighscores()

        # Renew resultscreen with current score winner.
        self.schermen['resultaat'] = [resultaatScherm(self, -1, currentScore[0]), (500, 350)]
        # Rebind buttons
        self.bindResultaat()
        self.setScherm('resultaat')
        self.game.player_info = {}
        currentScore = []

    def onScrabbleButton(self, event):
        current_object = event.GetEventObject()
        if not current_object.getTileStatus() and not (self.game.isHandEmpty() and current_object.getLetter() == ""):
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

    def bindResultaat(self): 
        scherm = self.schermen['resultaat'][0]
        scherm.backButton.Bind(wx.EVT_BUTTON, self.onResultaatButton)
        scherm.scoreBoardButton.Bind(wx.EVT_BUTTON, self.onResultaatButton)
        
    def bindPreGameOptions(self):
        scherm = self.schermen['spelSettings'][0]
        scherm.spelenButton.Bind(wx.EVT_BUTTON, self.onPreGameOptionsSpelenButton)
        scherm.backButton.Bind(wx.EVT_BUTTON, self.onPreGameOptionsTerugButton)

    def bindMenu(self):
        scherm = self.schermen['menu'][0]
        for button in scherm.buttons:
            button.Bind(wx.EVT_BUTTON, self.onMenuButton)

    def bindHighscores(self):
        scherm = self.schermen['highscores'][0]
        scherm.backButton.Bind(wx.EVT_BUTTON, self.onHighscoreButton)
        scherm.csvButton.Bind(wx.EVT_BUTTON, self.onHighscoreButton)

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
    
    def onWisselButton(self, event):
        letters = self.game.getPlayerLetters()
        self.onClearButton(event)
        test = InwisselPopup(letters, icon_path="./Media/")
        test.ShowModal()
        if test.weggooiLetters:
            for x in test.weggooiLetters:
                self.game.playLetter(letters[x])
            self.game.nextTurn(True)
            self.refreshInfo()
        else:
            pass
        test.Destroy()

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
        score_list, validTrun, statusList, position_list, valid_letters, possible_lone_letters = [], True, [], [], [], {}
        for y in range(len(self.schermen['speelbord'][0].button_grid)):
            for x in range(len(self.schermen['speelbord'][0].button_grid[y])):
                if self.schermen['speelbord'][0].button_grid[y][x].getLetter() != "":
                    lone_letter_count, horizontal_check, vertical_check, lone_letter_woorden = 0, False, False, []
                    if not x > 13 and self.getNextTileLetter((x, y), True) != "":
                        horizontal_check = True
                        tb_status, tb_woord, tb_score, word_pos, letters_in_woord, pos_lone_letter_pos = self.checkForWoord((x, y), True)
                        print("({:2}, {:2}) hor: {}; status = {:10}, woord = '{}'".format(x, y, True, tb_status, tb_woord))
                        if tb_status == "loneLetter":
                            if self.game.getAantalLettersGespeeld() != 1:
                                lone_letter_count += 1
                                lone_letter_woorden.append((tb_woord, tb_score))
                                lone_letter_pos = pos_lone_letter_pos
                            else:
                                position_list.append(word_pos)
                                score_list.append([tb_woord, tb_score])
                        else:
                            statusList.append(tb_status)
                        if tb_status == "notNew":
                            horizontal_check = False
                            valid_letters = valid_letters + letters_in_woord
                        elif tb_status == "ok":
                            valid_letters = valid_letters + letters_in_woord
                            position_list.append(word_pos)
                            score_list.append([tb_woord, tb_score])
                        elif self.game.isFirstTurn():
                            if tb_status == "notInMiddle":
                                position_list.append(word_pos)
                        else:
                            if tb_status == "notConnected":
                                position_list.append(word_pos)

                    if not y > 13 and self.getNextTileLetter((x, y), False) != "":
                        vertical_check = True
                        tb_status, tb_woord, tb_score, word_pos, letters_in_woord, pos_lone_letter_pos = self.checkForWoord((x, y), False)
                        print("({:2}, {:2}) hor: {}; status = {:10}, woord = '{}'".format(x, y, False, tb_status, tb_woord))
                        if tb_status == "loneLetter":
                            if self.game.getAantalLettersGespeeld() != 1:
                                lone_letter_count += 1
                                lone_letter_woorden.append((tb_woord, tb_score))
                                lone_letter_pos = pos_lone_letter_pos
                            else:
                                position_list.append(word_pos)
                                score_list.append([tb_woord, tb_score])
                        else:
                            statusList.append(tb_status)
                        if tb_status == "notNew":
                            vertical_check = False
                            valid_letters = valid_letters + letters_in_woord
                        elif tb_status == "ok":
                            valid_letters = valid_letters + letters_in_woord
                            position_list.append(word_pos)
                            score_list.append([tb_woord, tb_score])
                        elif self.game.isFirstTurn():
                            if tb_status == "notInMiddle":
                                position_list.append(word_pos)
                        else:
                            if tb_status == "notConnected":
                                position_list.append(word_pos)
                    if horizontal_check and vertical_check:
                        if lone_letter_count > 0:
                            print("possible lone letter added on ({}, {}) checks = ({}, {})".format(lone_letter_pos[0], lone_letter_pos[1], horizontal_check, vertical_check))
                            possible_lone_letters[lone_letter_pos] = lone_letter_woorden
                    elif (horizontal_check or vertical_check) and lone_letter_count > 0:
                        print("possible lone letter added on ({}, {}) checks = ({}, {})".format(lone_letter_pos[0], lone_letter_pos[0], horizontal_check,
                                                                                       vertical_check))
                        possible_lone_letters[lone_letter_pos] = lone_letter_woorden
                    elif lone_letter_woorden:
                        for (woord, score) in lone_letter_woorden:
                            score_list.append([woord, score])
                    # elif not horizontal_check and not vertical_check and not self.schermen['speelbord'][0].button_grid[y][x].getTileStatus():
                    #     print("lone letter added on ({}, {})".format(x, y))
                    #     statusList.append("loneLetter")
        for lone_letter_position in possible_lone_letters:
            if lone_letter_position not in valid_letters:
                statusList.append("loneLetter")
                print("!!!! loneletter added {}".format(lone_letter_position))
            else:
                for (woord, score) in possible_lone_letters[lone_letter_position]:
                    score_list.append([woord, score])


        print(statusList.count("loneLetter"))
        if "loneLetter" in statusList:
            dlg = wx.MessageDialog(self,
                                   "There are still lone letters on the board.",
                                   "Lose letters",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if len(position_list) != len(set(position_list)):
            # als er twee geldige woorden op dezelfde lijn worden gespeeld
            dlg = wx.MessageDialog(self, "You can only place one word.", "Multiple words",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if "notConnected" in statusList:
            # als er woorden niet aan oude letters liggen na de eerste beurt
            dlg = wx.MessageDialog(self, "New words must connect to old ones.", "Word not connected",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if "notInMiddle" in statusList:
            # als de letters niet in het midden liggen tijdens de eerste beurt
            dlg = wx.MessageDialog(self, "Must place first word in middle.", "Word not in middle", wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
            return
        if score_list:
            all_words_exist, false_woord = True, ""
            for (woord, score) in score_list:
                if not self.woordenboek.woordChecker(woord):
                    all_words_exist = False
                    false_woord = woord
            if all_words_exist:
                if self.game.isHandEmpty():
                    score_list.append(["Bonus", 50])
                self.game.addScore(score_list)
                self.lockLetters()
                self.game.nextTurn()
                self.refreshInfo()
            else:
                dlg = wx.MessageDialog(self, "'{}' is not a word.".format(false_woord), "Word not found",
                                       wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
                return


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
                        if self.getNextTileLetter((x, y), orientation) not in ["", None] or \
                                self.getPreviousTileLetter((x, y), orientation) not in ["", None]:
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
        woord, new, new_letters, woordMulti, woord_score, x, y, middle, connected = "", False, 0, 1, 0, pos[0], pos[1], False, False
        letters_in_woord = []
        new_letter_positions = []
        while True:
            letters_in_woord.append((x, y))
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
                    connected = True
                new = True
                new_letters += 1
                print("new letter position ({}, {})".format(x, y))
                new_letter_positions.append((x, y))
            if (y > 13 if not horizontal else False) or (x > 13 if horizontal else False):
                break
            if self.getNextTileLetter((x, y), horizontal) == "":
                break
            if horizontal:
                x += 1
            else:
                y += 1
        return new, new_letters, woord, woordMulti, woord_score, middle, connected, letters_in_woord, new_letter_positions

    def checkForWoord(self, pos, horizontal):
        if self.getPreviousTileLetter(pos, horizontal) == "" or (horizontal and pos[0] == 0) or (not horizontal and pos[1] == 0):
            new, new_letters, woord, woordMulti, woord_score, middle, connected, letters_in_woord, new_letter_positions = self.findWoord(pos, horizontal)
            score = woord_score * woordMulti
            if new:
                if self.game.isFirstTurn() and not middle:
                    return "notInMiddle", woord, 0, (horizontal, pos[1] if horizontal else pos[0]), letters_in_woord, (-1, -1)
                if not self.game.isFirstTurn() and not connected:
                    return "notConnected", woord, 0, (horizontal, pos[1] if horizontal else pos[0]), letters_in_woord, (-1, -1)
                if new_letters == 1:
                    return "loneLetter", woord, score, (horizontal, pos[1] if horizontal else pos[0]), letters_in_woord, new_letter_positions[0]
                return "ok", woord, score, (horizontal, pos[1] if horizontal else pos[0]), letters_in_woord, (-1, -1)
        return "notNew", "Error", 0, (horizontal, pos[1] if horizontal else pos[0]), [], (-1, -1)

    def refreshInfo(self):
        self.schermen['speelbord'][0].speler.SetLabel(self.game.getCurrentPlayer())
        self.schermen['speelbord'][0].score.SetLabel(str(self.game.getCurrentScore()))
        self.schermen['speelbord'][0].beurtLetters.SetLabel(str(self.game.getAantalLettersGespeeld()))
        self.schermen['speelbord'][0].hand.changeHand(self.game.getPlayerLetters())
        self.schermen['speelbord'][0].textbox.SetValue("\n".join(self.game.getLog()))
        self.setScherm('speelbord')
        if self.game.isLettersEmpty():
            self.schermen['speelbord'][0].wisselButton.SetLabel("Beurt overslaan")

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
        if "" in namen:
            dlg = wx.MessageDialog(self, "Names cannot be empty.", "Empty name",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        elif len(set(namen)) != len(namen):
            dlg = wx.MessageDialog(self, "All names must be unique.", "Duplicate name",
                                   wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()
        else:
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
        elif object.GetId() == 2:
            dialog = wx.FileDialog(
                self, "Save CSV file", wildcard="CSV files (*.csv)|*.csv",
                style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_CANCEL:
                return
            paths = dialog.GetPaths()
            dialog.Destroy()
            if len(paths) != 0:
                with open(paths[0], "w") as output:
                    writer = csv.writer(output, lineterminator='\n')
                    writer.writerows(self.schermen['highscores'][0].scoreData)

    def onResultaatButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('menu')
        elif object.GetId() == 2:
            self.setScherm('highscores')
    
    def onPreGameButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('menu')
        elif object.GetId() == 2:
            self.setScherm('speelbord')

    def onSettingsButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('menu')
        elif object.GetId() == 2:
            self.setScherm('woordenToevoeg')
        elif object.GetId() == 3:
            self.setScherm('woordenVerwijder')

    def onToevoegButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('settings')
        if object.GetId() == 2:
            print("Toevoeg woord: " +
                self.schermen['woordenToevoeg'][0].textBox.GetValue().lower())

    def onVerwijderButton(self, event):
        object = event.GetEventObject()
        if object.GetId() == 1:
            self.setScherm('settings')
        if object.GetId() == 2:    
            print("Verwijder woord: " +
                  self.schermen['woordenVerwijder'][0].textBox.GetValue().lower())

if __name__ == "__main__":
    app = wx.App()
    Schermpje2(None, -1, "Scrabble!")
    app.MainLoop()

