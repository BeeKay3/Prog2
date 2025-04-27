# -------------------   Developers   --------------------

# Artiom Triboi        - artiom.triboi@stud.th-deg.de
# Bikalpa Khachhibhoya - bikalpa.khachhibhoya@stud.th-deg.de
# Seifalislam Sebak    - seifalislam.sebak@stud.th-deg.de


import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import pyocr
import pyocr.builders
import threading
import team_Artiom_Bikalpa_Seifalislam_controller as controller

class window(tk.Tk):
    def __init__(self, title, resolution=None):
        super().__init__()
        self.title(title)
        if resolution is None:
            self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')
        else:
            self.geometry(resolution)
        self.minsize(width=1200, height=720)

class childWindow(tk.Toplevel):
    def __init__(self, parent, title, resolution):
        super().__init__(takefocus=True)
        self.title(title)
        self.geometry(resolution)
        self.attributes('-topmost', 1)
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
        statusLabel.config(font=('Arial', 10, 'bold'))
        statusLabel.grid(row=4, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5)
        
        self.availableVar = tk.BooleanVar()
        self.lendoutVar = tk.BooleanVar()
        self.missingVar = tk.BooleanVar()
        self.deletedVar = tk.BooleanVar()
        availableCheckbox = ttk.Checkbutton(self, text='available', variable=self.availableVar)
        availableCheckbox.grid(row=5, column=0, sticky=tk.EW, padx=5, pady=5)
        lendoutCheckbox = ttk.Checkbutton(self, text='lend out', variable=self.lendoutVar, padding=(60, 0, 0, 0))
        lendoutCheckbox.grid(row=5, column=1, sticky= tk.EW, padx=5, pady=5)
        missingCheckbox = ttk.Checkbutton(self, text='missing', variable=self.missingVar)
        missingCheckbox.grid(row=6, column=0, sticky=tk.EW, padx=5, pady=5)
        deletedCheckbox = ttk.Checkbutton(self, text='deleted', variable=self.deletedVar, padding=(60, 0, 0, 0))
        deletedCheckbox.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)
        
        searchButton = ttk.Button(self, text='Search (clear search results)', command=self.search)
        searchButton.grid(row=7, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=25)
        ocrSearchButton = ttk.Button(self, text='OCR Search', command=self.ocrSearch)
        ocrSearchButton.grid(row=8, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=(0, 25))
        addButton = ttk.Button(self, text='Add Book', command=self.addBook)
        addButton.grid(row=9, column=0, sticky=tk.EW, padx=5, pady=10)
        addmillionButton = ttk.Button(self, text='Add 1 Million Books', command=self.addmillionConfirm)
        addmillionButton.grid(row=9, column=1, sticky=tk.E, padx=5, pady=10)

    def addBook(self):
        root = childWindow(self.root, 'Add book', '300x300')
        front = addBookMenu(root, self.control, self.table, "", "")
        front.pack(padx=10, pady=10)
        root.wait_window()

    def addmillionConfirm(self):
        value = tk.messagebox.askyesno(title='confirmation', message='Are you sure that you want to add a million entries?')
        if value:
            root = childWindow(self.root, "Status", "500x200")
            front = millionStatusMenu(root, self.control)
            front.pack(padx=10, pady=10)
            root.wait_window()
            
            self.control.extendMillion()
            self.table.clearTable()
            tk.messagebox.showinfo(title="Done", message="Process Complete\nPlease wait while the table updates")
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

    def ocrSearch(self):
        filetype = [('Image files', '*.png'), ('Image files', '*.jpg'), ('Image files', '*.jpeg')]
        self.filename = filedialog.askopenfilename(title='Open Image File', initialdir='.', filetypes=filetype)
        if self.filename == () or self.filename == '':
            tk.messagebox.showerror(title="Error", message="File not selected")
        else:
            self.ocrSearchWindow = imageDrawer(self.root, self.control, self.table, self.filename)


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
        self.books.column('1', width=100, stretch=False, anchor=tk.CENTER)
        self.books.heading('2', text='Title')
        self.books.column('2', width=200, stretch=True)
        self.books.heading('3', text='Author')
        self.books.column('3', width=200, stretch=True)
        self.books.heading('4', text='Year')
        self.books.column('4', width=100, stretch=False, anchor=tk.CENTER)
        self.books.heading('5', text='Status')
        self.books.column('5', width=150, stretch=False, anchor=tk.CENTER)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.books.yview)
        self.books.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        self.books.pack(side=tk.LEFT, anchor=tk.NW, pady=10, expand=True, fill=tk.BOTH)
        
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
        root = childWindow(self.root, 'Change status', '200x200')
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

    def __init__(self, parent, control, table, title, author):
        super().__init__(parent)
        self.root = parent
        self.root.grab_set()
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
        self.titleEntry.insert(0, title)
        
        authorLabel = ttk.Label(fields, text='Author:')
        authorLabel.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.authorEntry = ttk.Entry(fields, width=25)
        self.authorEntry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.authorEntry.insert(0, author)
        
        yearLabel = ttk.Label(fields, text='Year:')
        yearLabel.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.yearEntry = ttk.Entry(fields, width=25)
        self.yearEntry.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)
        
        statusLabel = ttk.Label(fields, text='Select Status:')
        statusLabel.config(font=('Arial', 10))
        statusLabel.grid(row=4, column=0, columnspan=2, padx=5, pady=10)
        
        self.statusVar = tk.StringVar()
        availableRadiobox = ttk.Radiobutton(buttons, text='available', value='available', variable=self.statusVar)
        availableRadiobox.grid(row=5, column=0, sticky=tk.EW, padx=5, pady=5)
        lendoutRadiobox = ttk.Radiobutton(buttons, text='lend out', value='lend out', variable=self.statusVar)
        lendoutRadiobox.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)
        missingRadiobox = ttk.Radiobutton(buttons, text='missing', value='missing', variable=self.statusVar)
        missingRadiobox.grid(row=6, column=0, sticky=tk.EW, padx=5, pady=5)
        deletedRadiobox = ttk.Radiobutton(buttons, text='deleted', value='deleted', variable=self.statusVar)
        deletedRadiobox.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)
        
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
        self.root.grab_set()
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
        lendoutRadiobox.grid(row=5, column=1, sticky=tk.EW, padx=5, pady=5)
        missingRadiobox = ttk.Radiobutton(buttons, text='missing', value='missing', variable=self.statusVar)
        missingRadiobox.grid(row=6, column=0, sticky=tk.EW, padx=5, pady=5)
        deletedRadiobox = ttk.Radiobutton(buttons, text='deleted', value='deleted', variable=self.statusVar)
        deletedRadiobox.grid(row=6, column=1, sticky=tk.EW, padx=5, pady=5)
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

class millionStatusMenu(ttk.Frame):
    
    def __init__(self, parent, control):
        super().__init__(parent)
        self.root = parent
        self.control = control
        self.root.grab_set()
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        
        statusLabel = ttk.Label(self, text="Adding Entries Please Wait")
        statusLabel.config(font=("Arial", 20))
        statusLabel.pack(padx=5, pady=5)
        
        self.root.update_idletasks()
        pb = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=self.root.winfo_width())
        pb.pack(padx=5, pady=20)
        pb.start()
        
        stopButton = ttk.Button(self, text="Cancel", command=self.stop)
        stopButton.pack(padx=5, pady=5)
        
        t1 = threading.Thread(target=self.control.addMillion)
        t1.start()
        self.monitor(t1)
    
    def monitor(self, thread):
        if thread.is_alive():
            self.after(50, lambda: self.monitor(thread))
        else:
            self.root.destroy()
    
    def stop(self):
        self.control.stopMillion(True)     

class mainView:

    def __init__(self, root):
        self.root = root
        self.control = controller.libraryController()
        self.control.openJson("team_Artiom_Bikalpa_Seifalislam_lib_default.json")
        
        Menubar = tk.Menu(self.root)
        self.root.config(menu=Menubar)
        fileMenu = tk.Menu(Menubar, tearoff=0)
        fileMenu.add_command(label='Open Existing Library', command=self.openFile)
        fileMenu.add_command(label='Create New Library', command=self.newFile)
        Menubar.add_cascade(label='File', menu=fileMenu)
        self.LibraryDetails = libraryDetails(root, self.control)
        Menu = mainMenu(root, self.control, self.LibraryDetails)
        Menu.pack(side=tk.LEFT, anchor=tk.NW, padx=10, pady=10)
        self.LibraryDetails.pack(side=tk.LEFT, anchor=tk.NW, padx=25, pady=10, expand=True, fill=tk.BOTH)


    def openFile(self):
        filetype = [('json files', '*.json')]
        self.filename = filedialog.askopenfilename(title='Open Existing Library', initialdir='.', filetypes=filetype)
        if self.filename == () or self.filename == '':
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
        root = childWindow(self.root, 'Create a new library', '400x125')
        root.grab_set()
        name_var = tk.StringVar()
        nameLabel = ttk.Label(root, text='File name (no extension needed): ')
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


class imageDrawer:
    def __init__(self, parent, control, table, image_path):
        self.root = parent
        self.control = control
        self.table = table

        mainw = tk.Toplevel()
        mainw.title("Image to text - Draw a rectangle on image")
        
        self.canvas = tk.Canvas(mainw, width=450, height=600)
        self.canvas.pack()  
        self.image = Image.open(image_path).resize((450, 600))
        self.image_tk = ImageTk.PhotoImage(self.image.resize((450, 600)))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.size_label = tk.Label(mainw, text="To recognize the text in image select it by drawing a rectangle", font=("Helvetica", 12))
        self.size_label.pack(pady=10)
        self.text_label = tk.Label(mainw, text="", font=("Helvetica", 12))
        self.text_label.pack(pady=10)

        tools = pyocr.get_available_tools()
        if len(tools) == 0:
            raise Exception("No OCR tool found")
        self.tool = tools[0]

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        mainw.mainloop()

    def on_button_press(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_mouse_drag(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        
        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.size_label.config(text=f"Dimensions: {width} x {height}")

    def on_button_release(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        self.canvas.itemconfig(self.rect, outline="light green", width=3)


        width = abs(event.x - self.start_x)
        height = abs(event.y - self.start_y)
        self.size_label.config(text=f"Dimensions: {width} x {height}")

        self.recognize_text_in_rectangle(self.start_x, self.start_y, event.x, event.y, width, height)

    def addBook(self, text, option):
        root = childWindow(self.root, 'Add book', '300x300')
        if option == 1:
            front = addBookMenu(root, self.control, self.table, text, "")
        else:
            front = addBookMenu(root, self.control, self.table, "", text)
        front.pack(padx=10, pady=10)
        root.wait_window()

    def recognize_text_in_rectangle(self, x1, y1, x2, y2, width, height):
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        if width == 0 or height == 0:
            self.text_label.config(text=f"Recognized Text:\nSelect a valid area!")
        else:
            cropped_image = self.image.crop((x1, y1, x2, y2))
            recognized_text = self.tool.image_to_string(cropped_image, lang='eng', builder=pyocr.builders.TextBuilder())
            if recognized_text.strip() == "":
                self.text_label.config(text=f"Recognized Text:\nText not found!")
            else:
                self.text_label.config(text=f"Recognized Text: {recognized_text.strip()}") 
                self.control.ocrSearchBook(recognized_text.strip())
                self.table.clearTable()
                self.table.updateTableSearch()
                if not self.table.books.get_children():
                    response = tk.messagebox.askyesno("Book not found", "Book now found. Would you like to create a new record?")
                    if response:
                        option = tk.messagebox.askyesno("Recognized Text", "Book now found. Is the recognized text the title of the book?")
                        if option:
                            self.addBook(recognized_text.strip(), 1)
                        else:
                            self.addBook(recognized_text.strip(), 2)
