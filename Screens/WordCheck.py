class WordCheck:
    def __init__ (self):
        self.path = "./"
        file = open("woorden.lst","r")
        self.lst_woorden = file.read().splitlines()
        file.close()
        self.lst_woorden = self.lst_woorden[5:]


    def woordChecker(self, str_woord):
        if str_woord in self.lst_woorden:
            return True
        else:
            return False

    def woordToevoegen(self, str_woord):
        if str_woord in self.lst_woorden:
            return "Dit woord staat al in de lijst."
        elif str_woord.len() < 3:
            return "Dit woord is te klein om toe te voegen."
        else:
            self.lst_woorden.append(str_woord)
            return "OK"

    def woordVerwijderen(self, str_woord):
        if str_woord not in self.lst_woorden:
            return "Dit woord staat niet in de lijst."
        else:
            return "OK"





if __name__ == '__main__':
    Woord = WordCheck()
