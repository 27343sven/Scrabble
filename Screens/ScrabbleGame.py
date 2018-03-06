from random import shuffle

class ScrableGame:
    def __init__(self, default_letters=7):
        # letter frequenties
        self.standard_letters = {"a": 6, "b": 2, "c": 2, "d": 5,
                                 "e": 18, "f": 2, "g": 3, "h": 2,
                                 "i": 4, "j": 2, "k": 3, "l": 3,
                                 "m": 3, "n": 10, "o": 6, "p": 2,
                                 "q": 1, "r": 5, "s": 5, "t": 5,
                                 "u": 3, "v": 2, "w": 2, "x": 1,
                                 "y": 1, "ij": 2, "z": 2}
        self.letters = self.fillLetters()
        self.players = []
        self.player_info = {}
        self.current_player = ""
        self.current_beurt = 1
        self.letters_gespeeld = 0
        self.default_letters = default_letters
        self.log = []

    def fillLetters(self):
        letters = []
        for letter in self.standard_letters:
            letters += [letter] * self.standard_letters[letter]
        shuffle(letters)
        return letters

    def addScore(self, score_list):
        self.log.append("==={}===".format(self.current_player))
        for woord, score in score_list:
            self.log.append("{}\t{}".format(woord,score))
            self.player_info[self.current_player]['score'] += score

    def getPlayerLetters(self):
        return list(self.player_info[self.current_player]['letters'])

    def playLetter(self, letter):
        player_letters = self.player_info[self.current_player]['letters']
        return player_letters.pop(player_letters.index(letter))

    def clearLetter(self, letter):
        self.player_info[self.current_player]['letters'].append(letter)

    def refillPlayerLetters(self, player=""):
        if player == "":
            player = self.current_player
        while len(self.player_info[player]['letters']) < self.default_letters:
            new_letter = self.popLetter()
            if new_letter is not None:
                self.player_info[player]['letters'].append(new_letter)
            else:
                # als er geen letters meer over zijn
                break


    def popLetter(self):
        if self.letters:
            return self.letters.pop()
        else:
            return None

    def setPlayers(self, players):
        self.players = players
        for player in players:
            self.player_info[player] = {'letters': [self.popLetter() for x in range(self.default_letters)], 'score': 0}
        self.current_player = self.players[0]
        self.current_beurt = 1

    def nextTurn(self):
        index = self.players.index(self.current_player)
        self.refillPlayerLetters()
        if index + 1 >= len(self.players):
            self.current_player = self.players[0]
            self.current_beurt += 1
        else:
            self.current_player = self.players[index + 1]
        self.letters_gespeeld = 0

    def getCurrentBeurt(self):
        return self.current_beurt

    def getCurrentScore(self):
        return self.player_info[self.current_player]['score']

    def getAantalLettersGespeeld(self):
        return self.letters_gespeeld

    def getCurrentPlayer(self):
        return self.current_player

    def isHandFull(self):
        return True if len(self.letters) == self.default_letters else False

    def getLog(self):
        return self.log




if __name__ == '__main__':
    game = ScrableGame()
    game.setPlayers(['sven', 'steven', 'michael'])
