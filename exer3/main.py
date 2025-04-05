import model as md
import json

l = md.library()
err = ""
l.init("test12.json", err)
#print(l.addBook("asdfgh", "qwertyg", 1234, "loan"))
#print(l.deleteBook(1))
#print(l.updateStatus(1, "debt"))
print(l.lengthLib())
for x in l.allBooks():
    print(x)
print()
for x in l.searchBook(("loan"), "", "qwerty"):
    print(x)
