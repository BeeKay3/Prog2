import model
import random
import string

class libraryController:
    def openJson(self, filename):
        self.database = model.library()
        error = self.database.init(filename)
        if error is not None:
            return str(error)
        else:
            return True
    
    def getLibrary(self):
        return self.database.allBooks()
    
    def getLibraryName(self):
        return self.database.name.split("/")[-1]
    
    def getLibraryLength(self):
        return self.database.lengthLib()
        
    def updateBookStatus(self, index, value):
        self.database.updateStatus(index, value)
        self.database.save()
    
    def deleteBook(self, index):
        self.database.deleteBook(index)
        self.database.save()
    
    def searchBook(self, status, title, author, year):
        self.searchResults = []
        if year == "":
            year = 0
        else:
            year = int(year)
        for book in self.getLibrary():
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
                self.searchResults.append(book)
    
    def getSearchedLibrary(self):
        return self.searchResults
    
    def getIndex(self, book):
        return self.database.getIndex(book)
    
    def addBook(self, title, author, year, status):
        if title == "" or author == "" or year == "":
            return "field cannot be empty"
        elif not year.isnumeric():
            return "year must be a number"
        elif status == "":
            return "please choose a status"
        self.database.addBook(title, author, year, status)
        self.database.save()
        return True
    
    def addMillion(self):
        self.millionFlag = False
        self.tempLib = []
        states = ("available", "loan", "missing", "deleted")
        for x in range(500000):
            titleLength = random.randrange(5,16)
            authorLength = random.randrange(5,11)
            title = "".join(random.choice(string.ascii_letters) for i in range(titleLength))
            author = "".join(random.choice(string.ascii_letters) for i in range(authorLength))
            year = str(random.randrange(1800, 2026))
            status = states[random.randrange(0,4)]
            self.tempLib.append({"title": title, "author": author, "year": year, "status": status})
            if self.millionFlag:
                break
    
    def extendMillion(self):
        self.database.extendLib(self.tempLib)
        #self.database.save()
    
    def stopMillion(self, val):
        self.millionFlag = val
                
