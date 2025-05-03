# -------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de


import json
import random
import string

class library:
    currentLib = []

    def init(self, name):
        self.name = name
        try:
            with open(name, "r") as File:
                self.currentLib = json.load(File)
            return None
        except FileNotFoundError:
            self.currentLib = []
            return None
        except Exception as e:
            return e

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

    def deleteBook(self, index):
        self.currentLib.pop(index)
    
    def allBooks(self):
        return list(self.currentLib)
    
    def getBook(self, index):
        return self.currentLib[index].copy()
    
    def getIndex(self, val):
        return self.currentLib.index(val)

    def lengthLib(self):
        return len(self.currentLib)

    def updateStatus(self, index, state):
        self.currentLib[index].update(status= state)
    
    def extendLib(self, books):
        self.currentLib.extend(books)
