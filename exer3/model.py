import json

class library:
    def init(self, name, err):
        self.name = name
        try:
            with open(name, "r") as File:
                self.currentLib = json.load(File)
            err = None
            return True
        except FileNotFoundError:
            self.currentLib = []
            err = None
            return True
        except Exception as e:
            print(e)
            err = e
            return False

    def save(self):
        try:
            File = open(self.name, "w")
            json.dump(self.currentLib, File, indent = 4)
            File.close()
            return True
        except:
            return False

    def addBook(self, title, author, year, status):
        self.currentLib.append({"title": title, "author": author, "year": year, "status": status})
        return self.save()

    def deleteBook(self, index):
        self.currentLib.pop(index)
        return self.save()
    
    def allBooks(self):
        return list(self.currentLib)

    def lengthLib(self):
        return len(self.currentLib)

    def updateStatus(self, index, state):
        self.currentLib[index].update(status= state)
        return self.save()
