from Screens.SchermMenu import Schermpje as menuScherm
from Screens.SchermSettings import Schermpje as settingScherm
from Screens.SchermScorebord import Schermpje as highscoreScherm
from Screens.SchermWoordenToevoegen import Schermpje as woordenToevoegScherm
from Screens.SchermWoordenVerwijderen import Schermpje as woordenVerwijderScherm
from Screens.SchermPreGameOptions import Schermpje as spelSettingScherm
from Screens.SchermSpelbord import Schermpje as speelScherm
from Screens.SchermResultaat import Schermpje as resultaatScherm

# popups
from Screens.LetterInwisselScanner import Picker as letterInwisselPopup
from Screens.PopupLetterScanner import Picker as letterSelectiePopup

import wx
import csv

class Schermpje2(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1200, 600))
        self.schermen = {}
        self.initialiseerSchermen()
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
    Schermpje2(None, -1, "button")
    app.MainLoop()

