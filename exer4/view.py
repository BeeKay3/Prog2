import tkinter as tk
from tkinter import ttk, filedialog
import threading
import controller

class window(tk.Tk):

    def __init__(self, title, resolution=None):
        super().__init__()
        self.title(title)
        if resolution is None:
            self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')
        else:
            self.geometry(resolution)
        self.resizable(False, False)

class childWindow(tk.Toplevel):
    def __init__(self, parent, title, resolution):
        super().__init__(takefocus=True)
        self.title(title)
        self.geometry(resolution)
        self.resizable(False, False)

class mainMenu(ttk.Frame):

    def __init__(self, parent, control, table):
        super().__init__(parent)
        self.root = parent
        self.control = control
        self.table = table
        
        searchLabel = ttk.Label(self, text='Book Search')
        searchLabel.config(font=('Arial', 20))
        searchLabel.grid(row=0, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        titleLabel = ttk.Label(self, text='Title:')
        titleLabel.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.titleEntry = ttk.Entry(self, width=25)
        self.titleEntry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        authorLabel = ttk.Label(self, text='Author:')
        authorLabel.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.authorEntry = ttk.Entry(self, width=25)
        self.authorEntry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        yearLabel = ttk.Label(self, text='Year:')
        yearLabel.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.yearEntry = ttk.Entry(self, width=25)
        self.yearEntry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        statusLabel = ttk.Label(self, text='Select status to exclude:')
        statusLabel.config(font=('Arial', 10))
        statusLabel.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        self.availableVar = tk.BooleanVar()
        self.lendoutVar = tk.BooleanVar()
        self.missingVar = tk.BooleanVar()
        self.deletedVar = tk.BooleanVar()
        availableCheckbox = ttk.Checkbutton(self, text='available', variable=self.availableVar)
        availableCheckbox.grid(row=5, column=0, sticky=tk.EW, padx=5, pady=5)
        lendoutCheckbox = ttk.Checkbutton(self, text='lend out', variable=self.lendoutVar)
        lendoutCheckbox.grid(row=5, column=1, padx=5, pady=5)
        missingCheckbox = ttk.Checkbutton(self, text='missing', variable=self.missingVar)
        missingCheckbox.grid(row=6, column=0, sticky=tk.EW, padx=5, pady=5)
        deletedCheckbox = ttk.Checkbutton(self, text='deleted', variable=self.deletedVar)
        deletedCheckbox.grid(row=6, column=1, padx=5, pady=5)
        
        searchButton = ttk.Button(self, text='Search', command=self.search)
        searchButton.grid(row=7, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=25)
        addButton = ttk.Button(self, text='Add Book', command=self.addBook)
        addButton.grid(row=8, column=0, sticky=tk.EW, padx=5, pady=10)
        addmillionButton = ttk.Button(self, text='Add 1 Million Books', command=self.addmillionConfirm)
        addmillionButton.grid(row=8, column=1, sticky=tk.E, padx=5, pady=10)

    def addBook(self):
        root = childWindow(self.root, 'add book', '300x300')
        root.grab_set()
        front = addBookMenu(root, self.control, self.table)
        front.pack(padx=10, pady=10)
        root.wait_window()

    def addmillionConfirm(self):
        value = tk.messagebox.askyesno(title='confirmation', message='Are you sure that you want to add a million entries?')
        if value:
            t1 = threading.Thread(target=self.control.addMillion)
            t1.start()
            text = "Million Entries in Progress\nPress OK to continue\nPress Cancel to stop"
            confirm = tk.messagebox.askokcancel(title="Adding Million Entries", message=text)
            if not confirm:
                self.control.stopMillion(True)
            else:
                t1.join()
                self.control.extendMillion()
                self.table.clearTable()
                self.table.updateTable()

    def search(self):
        title = self.titleEntry.get()
        author = self.authorEntry.get()
        year =  self.yearEntry.get()
        status = []
        if self.availableVar.get(): status.append("available")
        if self.lendoutVar.get(): status.append("lend out")
        if self.missingVar.get(): status.append("missing")
        if self.deletedVar.get(): status.append("deleted")
        self.control.searchBook(status, title, author, year)
        self.table.clearTable()
        self.table.updateTableSearch()


class libraryDetails(ttk.Frame):

    def __init__(self, parent, control):
        super().__init__(parent)
        self.root = parent
        self.control = control
        
        self.libraryLabel = ttk.Label(self, text=f'Library: {self.control.getLibraryName()}')
        self.libraryLabel.config(font=('Arial', 20))
        self.libraryLabel.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=5)
        self.bookcountLabel = ttk.Label(self, text=f'No. of books: {self.control.getLibraryLength()}')
        self.bookcountLabel.config(font='Arial, 15')
        self.bookcountLabel.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=10)
        
        helptextLabel = ttk.Label(self, text='Press Enter to modify a record \nPress DEL to delete a record')
        helptextLabel.pack(side=tk.TOP, anchor=tk.NW, padx=5, pady=12)
        
        self.books = ttk.Treeview(self, columns=('1', '2', '3', '4', '5'), show='headings')
        self.books.heading('1', text='Number')
        self.books.column('1', width=50)
        self.books.heading('2', text='Title')
        self.books.heading('3', text='Author')
        self.books.heading('4', text='Year')
        self.books.column('4', width=50)
        self.books.heading('5', text='Status')
        self.books.column('5', width=100)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.books.yview)
        self.books.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        
        self.books.bind("<Return>", self.updateItem)
        self.books.bind("<Delete>", self.deleteConfirm)
        self.updateTable()
        
    def updateTable(self):
        self.libraryLabel.config(text=f"Library: {self.control.getLibraryName()}")
        self.bookcountLabel.config(text=f"No. of books: {self.control.getLibraryLength()}")
        for index, value in enumerate(self.control.getLibrary()):
            self.books.insert('', tk.END, text='', values=(index+1, value["title"], value["author"], value["year"], value["status"]))
        self.books.pack(side=tk.LEFT, anchor=tk.NW, pady=10, expand=True, fill=tk.BOTH)
    
    def updateTableSearch(self):
        for index, book in enumerate(self.control.getSearchedLibrary()):
            self.books.insert('', tk.END, text='', values=(index+1, book["title"], book["author"], book["year"], book["status"]))
            
    
    def clearTable(self):
        for book in self.books.get_children():
            self.books.delete(book)
    
    def updateItem(self, event):
        entry = self.books.selection()[0]
        root = childWindow(self.root, 'change status', '200x200')
        root.grab_set()
        front = changeStatusMenu(root, self.control)
        front.pack(padx=10, pady=10)
        val = self.books.item(entry)["values"]
        index = self.control.getIndex(val[1], val[2], val[3], val[4])
        root.wait_window()
        newStatus = front.getValue()
        if newStatus != "":
            self.control.updateBookStatus(index, newStatus)
            self.clearTable()
            self.updateTable()
        
    def deleteConfirm(self, event):
        if self.control.getLibraryLength() == 0:
            pass
        else:
            value = tk.messagebox.askyesno(title='confirmation', message='Are you sure that you want to delete this book?')
            if value:
                entry = self.books.selection()[0]
                val = self.books.item(entry)["values"]
                index = self.control.getIndex(val[1], val[2], val[3], val[4])
                self.control.deleteBook(index)
                self.clearTable()
                self.updateTable()

class addBookMenu(ttk.Frame):

    def __init__(self, parent, control, table):
        super().__init__(parent)
        self.root = parent
        self.control = control
        self.table = table
        fields = ttk.Frame(parent)
        buttons = ttk.Frame(parent)
        
        searchLabel = ttk.Label(fields, text='Add Book')
        searchLabel.config(font=('Arial', 20))
        searchLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        
        titleLabel = ttk.Label(fields, text='Title:')
        titleLabel.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.titleEntry = ttk.Entry(fields, width=25)
        self.titleEntry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        authorLabel = ttk.Label(fields, text='Author:')
        authorLabel.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.authorEntry = ttk.Entry(fields, width=25)
        self.authorEntry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        yearLabel = ttk.Label(fields, text='Year:')
        yearLabel.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.yearEntry = ttk.Entry(fields, width=25)
        self.yearEntry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        statusLabel = ttk.Label(fields, text='Select Status:')
        statusLabel.config(font=('Arial', 10))
        statusLabel.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        self.statusVar = tk.StringVar()
        availableRadiobox = ttk.Radiobutton(buttons, text='available', value='available', variable=self.statusVar)
        availableRadiobox.grid(row=0, column=0)
        availableRadiobox.grid(row=5, column=0, sticky=tk.EW, padx=5, pady=5)
        lendoutRadiobox = ttk.Radiobutton(buttons, text='lend out', value='lend out', variable=self.statusVar)
        lendoutRadiobox.grid(row=5, column=1, padx=5, pady=5)
        missingRadiobox = ttk.Radiobutton(buttons, text='missing', value='missing', variable=self.statusVar)
        missingRadiobox.grid(row=6, column=0, sticky=tk.EW, padx=5, pady=5)
        deletedRadiobox = ttk.Radiobutton(buttons, text='deleted', value='deleted', variable=self.statusVar)
        deletedRadiobox.grid(row=6, column=1, padx=5, pady=5)
        
        fields.pack(side=tk.TOP)
        buttons.pack(side=tk.TOP)
        
        addButton = ttk.Button(self.root, text='Add Book', command=self.addBook)
        addButton.pack(padx=5, pady=15)
    
    def addBook(self):
        title = self.titleEntry.get()
        author = self.authorEntry.get()
        year = self.yearEntry.get()
        status = self.statusVar.get()
        result = self.control.addBook(title, author, year, status)
        if result == True:
            tk.messagebox.showinfo(title="Success", message="Book added successfully")
            self.table.clearTable()
            self.table.updateTable()
            self.root.destroy()
        else:
            tk.messagebox.showerror(title="Error", message=result)

class changeStatusMenu(ttk.Frame):

    def __init__(self, parent, control):
        super().__init__(parent)
        self.root = parent
        self.control = control
        self.statusVar = tk.StringVar()
        buttons = ttk.Frame(self)
        
        statusLabel = ttk.Label(self, text='Select Status:')
        statusLabel.config(font=('Arial', 10))
        statusLabel.pack(padx=5, pady=5)
        
        availableRadiobox = ttk.Radiobutton(buttons, text='available', value='available', variable=self.statusVar)
        availableRadiobox.grid(row=0, column=0)
        availableRadiobox.grid(row=5, column=0, sticky=tk.EW, padx=5, pady=5)
        lendoutRadiobox = ttk.Radiobutton(buttons, text='lend out', value='lend out', variable=self.statusVar)
        lendoutRadiobox.grid(row=5, column=1, padx=5, pady=5)
        missingRadiobox = ttk.Radiobutton(buttons, text='missing', value='missing', variable=self.statusVar)
        missingRadiobox.grid(row=6, column=0, sticky=tk.EW, padx=5, pady=5)
        deletedRadiobox = ttk.Radiobutton(buttons, text='deleted', value='deleted', variable=self.statusVar)
        deletedRadiobox.grid(row=6, column=1, padx=5, pady=5)
        buttons.pack(padx=5, pady=5)
        
        searchButton = ttk.Button(self, text='Confirm', command = self.close)
        searchButton.pack(padx=5, pady=15)
    
    def getValue(self):
        return self.statusVar.get()
    
    def close(self):
        if self.statusVar.get() == "":
            tk.messagebox.showerror(title="Error", message="Please select an option!")
        else:
            self.root.destroy()


class mainView:

    def __init__(self, root):
        self.root = root
        self.control = controller.libraryController()
        self.control.openJson("lib_default.json")
        
        Menubar = tk.Menu(self.root)
        self.root.config(menu=Menubar)
        fileMenu = tk.Menu(Menubar, tearoff=0)
        fileMenu.add_command(label='Open Existing Library', command=self.openFile)
        fileMenu.add_command(label='Open a New Library', command=self.newFile)
        Menubar.add_cascade(label='File', menu=fileMenu)
        self.LibraryDetails = libraryDetails(root, self.control)
        Menu = mainMenu(root, self.control, self.LibraryDetails)
        Menu.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        self.LibraryDetails.pack(side=tk.LEFT, anchor=tk.NW, padx=25, pady=10, expand=True, fill=tk.BOTH)

    def openFile(self):
        filetype = [('json files', '*.json')]
        self.filename = filedialog.askopenfilename(title='Open Existing Library', initialdir='.', filetypes=filetype)
        if self.filename == ():
            tk.messagebox.showerror(title="Error", message="File not selected")
        else:
            result = self.control.openJson(self.filename)
            if result == True:
                tk.messagebox.showinfo(title="Success", message="File opened successfully")
            else:
                tk.messagebox.showerror(title="Error", message=result)
            self.LibraryDetails.clearTable()
            self.LibraryDetails.updateTable()

    def newFile(self):
        root = childWindow(self.root, 'create a new library', '400x125')
        root.grab_set()
        name_var = tk.StringVar()
        nameLabel = ttk.Label(root, text='Name: ')
        nameLabel.configure(font=('Arial', 15))
        nameLabel.pack(anchor=tk.CENTER, padx=5, pady=5)
        nameEntry = ttk.Entry(root, width=50, textvariable=name_var)
        nameEntry.pack(anchor=tk.CENTER, padx=5, pady=5)
        createButton = ttk.Button(root, text='Create', command=root.destroy)
        createButton.pack(anchor=tk.CENTER, padx=5, pady=10)
        root.wait_window()
        filename = name_var.get()
        if filename == "":
            tk.messagebox.showerror(title="Error", message="Filename not provided")
        else:
            result = self.control.openJson(filename+".json")
            if result == True:
                tk.messagebox.showinfo(title="Success", message="File opened successfully")
            else:
                tk.messagebox.showerror(title="Error", message=result)
            self.LibraryDetails.clearTable()
            self.LibraryDetails.updateTable()
