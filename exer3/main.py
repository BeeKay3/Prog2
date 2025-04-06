import model as md
import view as ui
import json

l = md.library()
err = ""
l.init("lib_default.json", err)

mainApp = ui.mainWindow(library=l)
l.updateStatus(mainApp.deleteRecord(), "deleted")


#print(l.addBook("asdfgh", "qwertyg", 1234, "loan"))
#print(l.deleteBook(1))
#print(l.updateStatus(1, "debt"))
#for x in l.allBooks():
#    print(x)
#print()
#for x in l.searchBook(("loan"), "", "qwerty"):
#    print(x)
