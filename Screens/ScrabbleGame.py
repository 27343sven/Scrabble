from random import shuffle

class ScrableGame:
    def __init__(self):
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
        print(self.letters)

    def fillLetters(self):
        letters = []
        for letter in self.standard_letters:
            letters += [letter] * self.standard_letters[letter]
        shuffle(letters)
        return letters

    def popLetter(self):
        if self.letters:
            return self.letters.pop()
        else:
            return None

    def setPlayers(self, players):
        self.players = players
        for player in players:
            self.player_info[player] = {'letters': [self.popLetter() for x in range(7)], 'score': 0}
        self.current_player = self.players[0]
        self.current_beurt = 1

    def nextTurn(self):
        index = self.players.index(self.current_player)
        if index + 1 >= len(self.players):
            self.current_player = self.players[0]
            self.current_beurt += 1
        else:
            self.current_player = self.players[index + 1]

    def getCurrentPlayer(self):
        return self.current_player



if __name__ == '__main__':
    game = ScrableGame()
    game.setPlayers(['sven', 'steven', 'michael'])
