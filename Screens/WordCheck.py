class WordCheck:
    def __init__ (self, path="../Media/", file="woorden.lst"):
        self.path = path
        file = open("{}{}".format(path, file), "r")
        self.lst_woorden = file.read().splitlines()
        file.close()
        self.lst_woorden = self.lst_woorden[1:]

    def woordChecker(self, str_woord):
        if str_woord in self.lst_woorden:
            return True
        else:
            return False

    def woordToevoegen(self, str_woord):
        if str_woord in self.lst_woorden:
            return "Dit woord staat al in de lijst."
        elif len(str_woord) < 3:
            return "Dit woord is te klein om toe te voegen."
        else:
            self.lst_woorden.append(str_woord)
            self.lst_woorden = sorted(self.lst_woorden, key=len)
            file = open("woorden.lst", "w")
            file.write(" \n\r")
            file.close()
            file = open("woorden.lst", "a")
            for word in self.lst_woorden:
                file.write(word+"\r\n")
            file.close()
            return "OK"

    def woordVerwijderen(self, str_woord):
        if str_woord not in self.lst_woorden:
            return "Dit woord staat niet in de lijst."
        else:
            self.lst_woorden.remove(str_woord)
            self.lst_woorden = sorted(self.lst_woorden, key=len)
            file = open("woorden.lst", "w")
            file.write(" \n\r")
            file.close()
            file = open("woorden.lst", "a")
            for word in self.lst_woorden:
                file.write(word + "\r\n")
            file.close()
            return "OK"






if __name__ == '__main__':
    Woord = WordCheck()
    print(Woord.woordVerwijderen("aag"))
    print(Woord.woordToevoegen("aagg"))
