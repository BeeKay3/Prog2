import json

class library:
    currentLib = []

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
    
    def getBook(self, index):
        return self.currentLib[index].copy()

    def lengthLib(self):
        return len(self.currentLib)

    def updateStatus(self, index, state):
        self.currentLib[index].update(status= state)
        return self.save()
    
    def searchBook(self, status, title=None, author=None, year=None):
        results = []
        for book in self.currentLib:
            result = True
            if title.lower != "" and not title.lower() in book["title"].lower():
                result = False
            else:
                if author != "" and not author.lower() in book["author"].lower():
                    result = False
                else:
                    if year != 0 and year != int(book["year"]):
                        result = False
                    else:
                        if status != None and book["status"] in status:
                            result = False

            if result == True:
                results.append(book)
        return results

    def addMillion(self):
        self.millionFlag = False
        tempLib = []
        states = ("available", "loan", "missing", "deleted")
        for x in range(1000000):
            titleLength = random.randrange(5,16)
            authorLength = random.randrange(5,11)
            title = "".join(random.choice(string.ascii_letters) for i in range(titleLength))
            author = "".join(random.choice(string.ascii_letters) for i in range(authorLength))
            year = str(random.randrange(1800, 2026))
            status = states[random.randrange(0,4)]
            tempLib.append({"title": title, "author": author, "year": year, "status": status})
            if self.millionFlag:
                return
        self.currentLib.extend(tempLib)

    def setFlag(self, val=True):
        self.millionFlag = val        
