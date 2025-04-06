# -------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de



# --------------------   Modules   --------------------

import json
import os
import team_Artiom_Bikalpa_Seifalislam_model as md
import tkinter as tk
from tkinter import ttk
import threading



class mainApp:

    #------------------------------ Controller functions ------------------------------

    def tableUpdate(self, library=None):
        self.nameLabel.config(text=f"Library:     {l.name}\nNumber of books:     {l.lengthLib()}")
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, book in enumerate(library, start=1):
            self.tree.insert("", "end", values=(i, book["title"], book["author"], book["year"], book["status"]))

    def placeholder(va=None):
        print("Placeholder used! Implement me >:(")

    def deleteRecord(self, deleteId):
        if deleteId != None:
            l.updateStatus(deleteId, "deleted")
        else:
            print("No item selected!")
        self.tableUpdate(l.allBooks())

    def searchShow(self):
        status = []
        if self.avlb.get() == 1:
            status.append("available")
        if self.lend.get() == 1:
            status.append("lend out")
        if self.miss.get() == 1:
            status.append("missing")
        if self.dltd.get() == 1:
            status.append("deleted")
        
        try:
            self.tableUpdate(l.searchBook(status, self.titl.get(), self.auth.get(), self.year.get()))
        except:
            self.year.set(0)
            self.tableUpdate(l.searchBook(status, self.titl.get(), self.auth.get(), self.year.get()))


    def addRecord(self):
        l.addBook(self.titla.get(), self.autha.get(), self.yeara.get(), self.statr.get())
        self.tableUpdate(l.allBooks())


    def modifyStatus(self, selectedRow, newStatus):
        l.updateStatus(selectedRow, newStatus.get())
        self.tableUpdate(l.allBooks())

    def millionCheck(self):
        while self.t1.is_alive():
           pass
        print("yes")
        self.millionkey = True       
        self.millionButton.config(text="Add a million entries")
        l.save()
        #self.tableUpdate(l.allBooks())
    
    def millionAdd(self):
        self.t1 = threading.Thread(target=l.addMillion)
        self.t2 = threading.Thread(target=self.millionCheck)
        if self.millionkey:
            self.millionkey = False
            self.millionButton.config(text="Cancel")
            self.t1.start()
            self.t2.start()
        else:
            l.setFlag(True)
            self.millionkey = True
            self.millionButton.config(text="Add a million entries")
            

    def fileOpen(self, fileName):
        l.init(fileName, err)
        self.name = fileName
        self.libl = l.lengthLib()
        self.tableUpdate(l.allBooks())
        self.nameLabel.config(text=f"Library:     {l.name}\nNumber of books:     {l.lengthLib()}")

    def newFile(self, fileName):
        l.init(f"{fileName}.json", err)
        self.name = l.name
        self.libl = l.lengthLib()
        self.tableUpdate(l.allBooks())
        self.nameLabel.config(text=f"Library:     {l.name}\nNumber of books:     {l.lengthLib()}")



    #------------------------------ View functions ------------------------------

    def mainWindow(self, library=None):
        mainw = tk.Tk()
        mainw.title("Exercise 3")
        mainw.geometry("1000x500")
        mainw.minsize(width=1000, height=500)
        mainw.grid_columnconfigure(1, weight=1)
        mainw.grid_rowconfigure(0, weight=1)


        #-------------------- Variables --------------------
        self.titl = tk.StringVar()
        self.auth = tk.StringVar()
        self.year = tk.IntVar()
        self.avlb = tk.IntVar()
        self.lend = tk.IntVar()
        self.miss = tk.IntVar()
        self.dltd = tk.IntVar()


        #-------------------- Window content --------------------
        leftFrame = tk.Frame(mainw, width=200)
        leftFrame.grid(row=0, column=0, sticky='ns')

        rightFrame = tk.Frame(mainw, width=1000)
        rightFrame.grid(row=0, column=1, sticky='nsew')
        rightFrame.grid_columnconfigure(0, weight=1)
        rightFrame.grid_rowconfigure(2, weight=1)

        menuBar = tk.Menu(mainw)
        mainw.config(menu=menuBar)
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open existing library", command=self.fileOpenWindow)
        fileMenu.add_command(label="Create new library", command=self.newFileWindow)
        menuBar.add_cascade(label="File", menu=fileMenu)

        tk.Label(leftFrame, text="Fields for searching a book:").grid(row=0, column=0, padx=10, pady=(25, 0))
        tk.Label(leftFrame, text="Title:").grid(row=1, column=0, padx=10, pady=(10, 0))
        tk.Entry(leftFrame, textvariable=self.titl, width=40, justify='center').grid(row=2, column=0, padx=10, pady=(0, 10))
        tk.Label(leftFrame, text="Author:").grid(row=3, column=0, padx=10, pady=(10, 0))
        tk.Entry(leftFrame, textvariable=self.auth, width=40, justify='center').grid(row=4, column=0, padx=10, pady=(0, 10))
        tk.Label(leftFrame, text="Year:").grid(row=5, column=0, padx=10, pady=(10, 0))
        tk.Spinbox(leftFrame, from_=0, to=2025, textvariable=self.year, justify='center').grid(row=6, column=0, padx=10, pady=(0, 10))

        tk.Label(leftFrame, text="Status (select which to exclude):").grid(row=7, column=0, padx=10, pady=(10, 0))
        tk.Checkbutton(leftFrame, text="Available", variable=self.avlb).grid(row=8, column=0, sticky='w', padx=(100, 0), pady=0)
        tk.Checkbutton(leftFrame, text="Lend out", variable=self.lend).grid(row=9, column=0, sticky='w', padx=(100, 0), pady=0)
        tk.Checkbutton(leftFrame, text="Missing", variable=self.miss).grid(row=10, column=0, sticky='w', padx=(100, 0), pady=0)
        tk.Checkbutton(leftFrame, text="Deleted", variable=self.dltd).grid(row=11, column=0, sticky='w', padx=(100, 0), pady=0)

        tk.Button(leftFrame, text="Search", width=20, command=self.searchShow).grid(row=12, column=0, padx=10, pady=(10, 0))
        tk.Button(leftFrame, text="Add a book", width=20, command=self.addWindow).grid(row=13, column=0, padx=10, pady=(20, 0))
        self.millionkey = True
        self.millionButton = tk.Button(leftFrame, text="Add 1 million books", width=20, command=self.millionAdd)
        self.millionButton.grid(row=14, column=0, padx=10, pady=(10, 0))

        self.nameLabel = tk.Label(rightFrame, text=f"Library:     {library.name}\nNumber of books:     {library.lengthLib()}", font=("Helvetica", 12), height=2, justify='left')
        self.nameLabel.grid(row=0, column=0, padx=10, pady=(20, 0), sticky='w')
        tk.Label(rightFrame, text=f"To modify a record double-click on it\nTo delete a record select it and right-click", height=2, justify='left').grid(row=1, column=0, padx=10, pady=10, sticky='w')


        self.tree = ttk.Treeview(rightFrame, columns=("Number", "Title", "Author", "Year", "Status"), show="headings", selectmode="browse")
        vscrollbar = ttk.Scrollbar(rightFrame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vscrollbar.set)
        vscrollbar.grid(row=2, column=0, padx=(0, 10), pady=(5, 25), sticky='nse')
        self.tree.grid(row=2, column=0, padx=10, pady=(5, 25), sticky='nsew')

        self.tree.heading("Number", text="Number")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Year", text="Year")
        self.tree.heading("Status", text="Status")
        self.tree.column("Number", width=50)
        self.tree.column("Title", width=300,  stretch=True)
        self.tree.column("Author", width=200)
        self.tree.column("Year", width=50)
        self.tree.column("Status", width=100)

        self.tree.bind("<Double-1>", lambda event: self.modifyWindow(self.tree.index(self.tree.selection()[0])))
        self.tree.bind("<Button-3>", lambda event: self.deleteWindow(self.tree.index(self.tree.selection()[0])))

        for i, book in enumerate(library.allBooks(), start=1):
            self.tree.insert("", "end", values=(i, book["title"], book["author"], book["year"], book["status"]))

        mainw.mainloop()



    def modifyWindow(self, selectedRow):
        mainw = tk.Toplevel()
        mainw.title("Modify book status")
        mainw.geometry("250x250")
        mainw.resizable(False, False)

        frame = tk.Frame(mainw)
        frame.pack(fill='both')

        
        bookStatus = tk.StringVar()
        bookStatus.set(l.allBooks()[selectedRow]["status"])

        tk.Label(frame, text="Select the new status:").pack(pady=(30, 10))
        tk.Radiobutton(frame, text="Available", variable=bookStatus, value="available").pack(anchor='w', padx=(100, 0))
        tk.Radiobutton(frame, text="Lend out", variable=bookStatus, value="lend out").pack(anchor='w', padx=(100, 0))
        tk.Radiobutton(frame, text="Missing", variable=bookStatus, value="missing").pack(anchor='w', padx=(100, 0))
        tk.Radiobutton(frame, text="Deleted", variable=bookStatus, value="deleted").pack(anchor='w', padx=(100, 0))
        tk.Button(frame, text="Save status change", width=20, command=lambda: [self.modifyStatus(selectedRow, bookStatus), mainw.destroy()]).pack(pady=10)

        mainw.mainloop()


    def deleteWindow(self, deleteId):
        mainw = tk.Toplevel()
        mainw.title("Delete book")
        mainw.geometry("350x150")
        mainw.resizable(False, False)

        frame = tk.Frame(mainw)
        frame.pack(fill='both')

        tk.Label(frame, text="Are you sure you want to delete this book?").pack(pady=(30, 10))
        tk.Button(frame, text="Yes", width=15, command=lambda: [self.deleteRecord(deleteId), mainw.destroy()]).pack(side='left', padx=30, pady=10)
        tk.Button(frame, text="No", width=15, command=mainw.destroy).pack(side='right', padx=30, pady=10)

        mainw.mainloop()


    def addWindow(self):
        mainw = tk.Toplevel()
        mainw.title("Exercise 3")
        mainw.geometry("300x400")
        mainw.resizable(False, False)

        #-------------------- Variables --------------------
        self.titla = tk.StringVar()
        self.autha = tk.StringVar()
        self.yeara = tk.IntVar(value=2025)
        self.statr = tk.StringVar(value="available")

        #-------------------- Window content --------------------
        leftFrame = tk.Frame(mainw, width=200)
        leftFrame.pack(fill='both', expand=True, padx=10, pady=10)

        tk.Label(leftFrame, text="Insert the data of the new book:").pack(pady=(10, 5))
        tk.Label(leftFrame, text="Title:").pack(anchor='center')
        tk.Entry(leftFrame, textvariable=self.titla, width=40, justify='center').pack(pady=5)
        tk.Label(leftFrame, text="Author:").pack(anchor='center')
        tk.Entry(leftFrame, textvariable=self.autha, width=40, justify='center').pack(pady=5)
        tk.Label(leftFrame, text="Year:").pack(anchor='center')
        tk.Spinbox(leftFrame, from_=0, to=2025, textvariable=self.yeara, justify='center').pack(pady=5)

        tk.Label(leftFrame, text="Status:").pack(anchor='center', pady=5)
        
        tk.Radiobutton(leftFrame, text="Available", variable=self.statr, value="available").pack(anchor='w', padx=(100, 0))
        tk.Radiobutton(leftFrame, text="Lend out", variable=self.statr, value="lend out").pack(anchor='w', padx=(100, 0))
        tk.Radiobutton(leftFrame, text="Missing", variable=self.statr, value="missing").pack(anchor='w', padx=(100, 0))
        tk.Radiobutton(leftFrame, text="Deleted", variable=self.statr, value="deleted").pack(anchor='w', padx=(100, 0))

        tk.Button(leftFrame, text="Add the book", width=20, command=lambda: [self.addRecord(), mainw.destroy()]).pack(pady=(20, 0))

        mainw.mainloop()


    def fileOpenWindow(self):
        mainw = tk.Toplevel()
        mainw.title("Open a library file")
        mainw.geometry("300x300")
        mainw.resizable(False, False)

        frame = tk.Frame(mainw)
        frame.pack(fill='both', expand=True)

        tk.Label(frame, text="Double-click the library file you want to open:").pack(pady=(20, 10))
        lstb = tk.Listbox(frame)
        lstb.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        lstb.bind('<Double-1>', lambda event: [self.fileOpen(lstb.get(lstb.curselection())), mainw.destroy()])

        for file in os.listdir("."):
            if file.endswith(".json"):
                lstb.insert('end', file)

        mainw.mainloop()


    def newFileWindow(self):
        mainw = tk.Toplevel()
        mainw.title("Create a new library file")
        mainw.geometry("400x150")
        mainw.resizable(False, False)

        frame = tk.Frame(mainw)
        frame.pack(fill='both', expand=True)

        fileName = tk.StringVar()

        tk.Label(frame, text="Enter the name of the new library file (no extension needed):").pack(pady=(20, 10))
        tk.Entry(frame, width=40, textvariable=fileName, justify='center').pack(pady=5)
        tk.Button(frame, text="Create", width=20, command=lambda: [self.newFile(fileName.get()), mainw.destroy()]).pack(pady=10)

        mainw.mainloop()





#------------------------------ Controller part ------------------------------

l = md.library()
err = "" 
l.init("team_Artiom_Bikalpa_Seifalislam_lib_default.json", err)
ma = mainApp()
ma.mainWindow(library=l)

