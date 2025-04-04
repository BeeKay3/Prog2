# --------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de



# --------------------   Modules   --------------------

import json
import os



# --------------------   Global variables   --------------------

work = '1'



# --------------------   Functions   --------------------

def Clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def Show():
    try:
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "r") as file:
            try:
                library = json.load(file)
                for element in library:
                    print("Book ID:  " + str(library.index(element) + 1))
                    print("Title:    " + element["title"])
                    print("Authors:  " + element["author"])
                    print("Year:     " + str(element["year"]))
                    print()
            except:
                print("\nLibrary is empty!\n")
    except FileNotFoundError:
        print("\nFile doesn't exist!\n")
    except:
        print("\nCouldn't open file\n")
        
    input("Press Enter to continue\n")


def AddBook():
    try:
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "r") as file:
            try:
                library = json.load(file)
            except:
                library = []
                print("\nAt the moment the library is empty\n")
    except FileNotFoundError:
        print("\nFile doesn't exist!\n")
        input("Press Enter to continue\n")
        return
    except:
        print("Couldn't open file\n")
        input("Press Enter to continue\n")
        return
    title = input("Enter the title - ")
    author = input("Enter the author - ")
    year = input("Enter the year - ")
    if not year.isnumeric():
        print("\nInput for year rejected - year must be numeric\n")
        input("Press Enter to continue")
        return
    library.append({"title": title, "author": author, "year": year})
    try:
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "w") as file:
            json.dump(library, file, indent = 4)
    except:
        print("Couldn't write in file\n")
        input("Press Enter to continue\n")
        return
    print("\nData saved in file successfully\n")
    input("Press Enter to continue\n")


def DeleteBook():
    try:
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "r") as file:
            try:
                library = json.load(file)
            except:
                print("\nLibrary is empty, there is nothing to delete\n")
                input("Press Enter to continue\n")
                return

        ID = input("Enter Book ID to Delete - ")

        if ID.isnumeric() == False or int(ID) < 0 or int(ID) > len(library):
            print("\nInvalid Book ID (you can check Book ID when displaying all books)\n")
            input("Press Enter to continue\n")
            return

        removed_book = library.pop(int(ID) - 1)
        print(f"\nDeletion successful: {removed_book['title']} by {removed_book['author']} ({removed_book['year']})\n")
        input("Press Enter to continue\n")

        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "w") as file:
            json.dump(library, file, indent=4)

    except FileNotFoundError:
        print("\nFile not found!\n")
        input("Press Enter to continue\n")
    except:
        print("\nCouldn't open file\n")
        input("Press Enter to continue\n")


def LibSort():
    try:
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "r") as file:
            try:
                library = json.load(file)
            except:
                print("\nLibrary is empty, there is nothing to sort\n")
                input("Press Enter to continue\n")
                return
    except FileNotFoundError:
        print("\nFile doesn't exist!\n")
    except:
        print("Couldn't open file\n")
        input("Press Enter to continue\n")
        return
    print("1 - Sort by Title")    
    print("2 - Sort by Authors")
    print("3 - Sort by Year")
    key = (input("\nEnter operation code - ")).strip()
    match key:
        case "1": library.sort(key = lambda e: e["title"])
        case "2": library.sort(key = lambda e: e["author"])
        case "3": library.sort(key = lambda e: e["year"])
        case _: 
            print("\nThis operation isn't valid\n")
            input("Press Enter to continue\n")
            return
    try:                                                 
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "w") as file:
            json.dump(library, file, indent = 4)
    except:
        print("Couldn't write in file\n")
        input("Press Enter to continue\n")
        return
    print("\nLibrary sorted successfully\n")
    input("Press Enter to continue\n")


def SearchBook():
    try:
        with open("team_Artiom_Bikalpa_Seifalislam_library.json", "r") as file:
            try:
                library = json.load(file)
            except:
                print("\nLibrary is empty, there is nothing to search\n")
                input("Press Enter to continue\n")
                return
    except FileNotFoundError:
        print("\nFile doesn't exist!\n")
    except:
        print("Couldn't open file\n")
        input("Press Enter to continue\n")
        return

    print("Write the parameters of the book you are looking for, in case you dont need one leave it empty and press Enter:")
    title = input("Title   - ")
    author = input("Authors - ")
    year = input("Year    - ")
    if year != "" and year.isnumeric() == False:
        print("\nInput for year rejected - year must be numeric\n")
        input("Press Enter to continue\n")
        return

    resultLibrary = []
    for book in library:
        result = True

        if title != "" and not title.lower() in book["title"].lower():
            result = False
        else:
            if author != "" and not author.lower() in book["author"].lower():
                result = False
            else:
                if year != "" and int(year) != int(book["year"]):
                    result = False

        if result == True:
            resultLibrary.append(book)

    if len(resultLibrary) == 0:
        print("\nNo results found\n")
        input("Press Enter to continue\n")
        return
    else:
        print("\nSearch results:")
        for book in resultLibrary:
            print("Book ID:  " + str(library.index(book) + 1))
            print("Title:    " + book["title"])
            print("Authors:  " + book["author"])
            print("Year:     " + str(book["year"]))
            print()
        input("Press Enter to continue\n")



# --------------------   Main code   --------------------

Clear()

while work != '0':
    Clear()

    if work.isnumeric() == False:
            print("\nThis operation isn't valid\n")
    else:
            if int(work) < 0 or int(work) > 5:
                print("\nThis operation isn't valid\n")

    print("Please enter the number of the needed operation:")
    print("1 - Display all books")
    print("2 - Add a new book")
    print("3 - Delete a book")
    print("4 - Sort the books")
    print("5 - Search a book")
    print("0 - Close the program")
    work = input("\nNeeded operation - ")
    work = work.strip()
    Clear()

    match work:
        case '1': Show()
        case '2': AddBook()
        case '3': DeleteBook()
        case '4': LibSort()
        case '5': SearchBook()
        case '0': continue

print("\nProgram finished successfully!\n\nHave a nice day :)\n")