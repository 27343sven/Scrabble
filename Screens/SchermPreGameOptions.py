import wx

class Schermpje(wx.Panel):

    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        boxje = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, -1, "Spel Opties")
        text.SetFont(wx.Font(30, wx.ROMAN, wx.NORMAL, wx.NORMAL))

        boxje.Add(text, 1, wx.CENTER)
        boxje.AddSpacer(40)
        boxje.Add(self.makeScherm(), 5, wx.CENTRE | wx.EXPAND)
        boxje.AddSpacer(40)
        boxje.Add(self.makeButtonBox(), 1, wx.BOTTOM | wx.EXPAND | wx.ALL)
        self.SetSizer(boxje) 

    def makeScherm(self):
        mainSizer = wx.BoxSizer()
        leftSizer = wx.BoxSizer(wx.VERTICAL)
        rightSizer = wx.BoxSizer(wx.VERTICAL)        
        leftSizer.Add(self.makePlayerOptionBox(), 1, wx.CENTER)
        rightSizer.Add(self.makeOptions(), 1, wx.CENTER)
        mainSizer.AddSpacer(30)
        mainSizer.Add(leftSizer, 1, wx.LEFT)
        mainSizer.Add(rightSizer, 1, wx.RIGHT)
        mainSizer.AddSpacer(30)    
        return mainSizer

    def makePlayerOptionBox(self):
        playerOptionSizer = wx.BoxSizer(wx.VERTICAL)
        self.playerOption = wx.RadioBox(self, -1, "Aantal Spelers:",
                                        choices=["2","3","4"], majorDimension=1) #Let op speleropties zijn string
        playerOptionSizer.Add(self.playerOption, 1, wx.LEFT)
        self.playerOption.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        return playerOptionSizer
        
    def makeOptions(self):
        self.tempBoxDict = {}   ##Box dictionary om later de static en control text te hiden
        self.textCtrlDict = {}  ##textCtrl dictionary voor de spelernamen
        mainBox = wx.BoxSizer()
        spelerNaamSizer = wx.BoxSizer(wx.VERTICAL)
        for x in range(4):
            tempBox = wx.BoxSizer()
            tempBox.Add(wx.StaticText(self, -1, "Speler {}".format(x+1)), wx.CENTER)
            self.textCtrlDict["textCtrl{0}".format(x+1)] = wx.TextCtrl(self, -1) #Add aan dict beginnend met "textctrl1"
            tempBox.Add(self.textCtrlDict["textCtrl{}".format(x+1)], wx.CENTER)
            self.tempBoxDict["box{0}".format(x+1)] = tempBox #Same maar voor tempBox
            spelerNaamSizer.Add(tempBox, wx.CENTER)
            spelerNaamSizer.AddSpacer(10)
        self.tempBoxDict["box3"].ShowItems(show=False)
        self.tempBoxDict["box4"].ShowItems(show=False)
        mainBox.AddSpacer(40)
        mainBox.Add(spelerNaamSizer, wx.RIGHT)
        return mainBox

    def makeButtonBox(self):
        buttonSizer = wx.BoxSizer()
        self.backButton = wx.Button(self, 1, "Terug")
        self.spelenButton = wx.Button(self, 2, "Spelen")
        self.buttons = [self.backButton, self.spelenButton] #
        buttonSizer.Add(self.backButton, 1, wx.LEFT)
        buttonSizer.Add(wx.Panel(self, -1), 1,wx.CENTER)
        buttonSizer.Add(self.spelenButton, 1, wx.RIGHT)
        return buttonSizer

    ##Basically hide de textvelden om het juiste aantal spelers te geven.
    ##Leegt ook de value van de ctrlText van de gehidede(?) velden.
    ##Eventueel in de controller plaatsen.
    def onRadioBox(self,e):
        label = self.playerOption.GetStringSelection()
        if label == "2":
            self.tempBoxDict["box3"].ShowItems(show=False)
            self.tempBoxDict["box4"].ShowItems(show=False)
            self.textCtrlDict["textCtrl3"].SetValue("")
            self.textCtrlDict["textCtrl4"].SetValue("")
        elif label == "3":
            self.tempBoxDict["box3"].ShowItems(show=True)
            self.tempBoxDict["box4"].ShowItems(show=False)
            self.textCtrlDict["textCtrl4"].SetValue("")
        elif label == "4":
            self.tempBoxDict["box3"].ShowItems(show=True)
            self.tempBoxDict["box4"].ShowItems(show=True)
        self.Layout()

    def center(self, item):
        vbox = wx.BoxSizer()
        hbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(item, 1, wx.CENTRE)
        hbox.Add(vbox, 1, wx.CENTRE)   
        return(hbox)

if __name__ == "__main__":
    class Naampje(wx.Frame):
        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, size=(400, 320),
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
