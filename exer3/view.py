import tkinter as tk




def placeholder(va=None):
    print("Placeholder used! Implement me >:(")


def mainWindow():
    mainw = tk.Tk()
    mainw.title("Exercise 3")
    mainw.geometry("1000x500")
    mainw.minsize(width=1000, height=500)
    mainw.grid_columnconfigure(1, weight=1)
    mainw.grid_rowconfigure(0, weight=1)


    #-------------------- Variables --------------------
    titl = tk.StringVar()
    auth = tk.StringVar()
    year = tk.IntVar()
    avlb = tk.IntVar()
    lend = tk.IntVar()
    miss = tk.IntVar()
    dltd = tk.IntVar()


    #-------------------- Window content --------------------
    leftFrame = tk.Frame(mainw, width=200)
    leftFrame.grid(row=0, column=0, sticky='ns')

    rightFrame = tk.Frame(mainw, width=1000)
    rightFrame.grid(row=0, column=1, sticky='nsew')
    rightFrame.grid_columnconfigure(0, weight=1)
    rightFrame.grid_rowconfigure(1, weight=1)

    menuBar = tk.Menu(mainw)
    mainw.config(menu=menuBar)
    fileMenu = tk.Menu(menuBar, tearoff=0)
    fileMenu.add_command(label="Open existing library", command=placeholder)
    fileMenu.add_command(label="Create new library", command=placeholder)
    menuBar.add_cascade(label="File", menu=fileMenu)

    tk.Label(leftFrame, text="Fields for searching a book:").grid(row=0, column=0, padx=10, pady=(25, 0))
    tk.Label(leftFrame, text="Title:").grid(row=1, column=0, padx=10, pady=(10, 0))
    tk.Entry(leftFrame, textvariable=titl, width=40, justify='center').grid(row=2, column=0, padx=10, pady=(0, 10))
    tk.Label(leftFrame, text="Author:").grid(row=3, column=0, padx=10, pady=(10, 0))
    tk.Entry(leftFrame, textvariable=auth, width=40, justify='center').grid(row=4, column=0, padx=10, pady=(0, 10))
    tk.Label(leftFrame, text="Year:").grid(row=5, column=0, padx=10, pady=(10, 0))
    tk.Spinbox(leftFrame, from_=0, to=2025, textvariable=year, justify='center').grid(row=6, column=0, padx=10, pady=(0, 10))

    tk.Label(leftFrame, text="Status:").grid(row=7, column=0, padx=10, pady=(10, 0))
    tk.Checkbutton(leftFrame, text="Available", variable=avlb).grid(row=8, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Lend out", variable=lend).grid(row=9, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Missing", variable=miss).grid(row=10, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Deleted", variable=dltd).grid(row=11, column=0, sticky='w', padx=(100, 0), pady=0)

    tk.Button(leftFrame, text="Search", width=20, command=placeholder).grid(row=12, column=0, padx=10, pady=(10, 0))
    tk.Button(leftFrame, text="Add a book", width=20, command=placeholder).grid(row=13, column=0, padx=10, pady=(20, 0))
    tk.Button(leftFrame, text="Add 1 million books", width=20, command=placeholder).grid(row=14, column=0, padx=10, pady=(10, 0))

    tk.Label(rightFrame, text=f"Library: xxx\nTotal number of books: xxx", font=("Helvetica", 12), height=2, justify='left').grid(row=0, column=0, padx=10, pady=(20, 0), sticky='w')
    lstb = tk.Listbox(rightFrame, font=("Helvetica", 14))
    lstb.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    lstb.bind('<Double-1>', placeholder)
    lstb.bind('<Button-3>', placeholder)
    tk.Label(rightFrame, text=f"To modify a record double-click on it\nTo delete a record right-click on it", height=2, justify='left').grid(row=2, column=0, padx=10, pady=(0, 20), sticky='w')

    for i in range(100):
        lstb.insert(i, f"Book {i + 1}")

    mainw.mainloop()



def modifyWindow(nowS):
    mainw = tk.Tk()
    mainw.title("Modify book status")
    mainw.geometry("250x250")
    mainw.resizable(False, False)

    frame = tk.Frame(mainw)
    frame.pack(fill='both')

    bookStatus = tk.IntVar()
    bookStatus.set(nowS)

    tk.Label(frame, text="Select the new status:").pack(pady=(30, 10))
    tk.Radiobutton(frame, text="Available", variable=bookStatus, value=1).pack(anchor='w', padx=(100, 0))
    tk.Radiobutton(frame, text="Lend out", variable=bookStatus, value=2).pack(anchor='w', padx=(100, 0))
    tk.Radiobutton(frame, text="Missing", variable=bookStatus, value=3).pack(anchor='w', padx=(100, 0))
    tk.Radiobutton(frame, text="Deleted", variable=bookStatus, value=4).pack(anchor='w', padx=(100, 0))
    tk.Button(frame, text="Save status change", width=20, command=placeholder).pack(pady=10)

    mainw.mainloop()


def deleteWindow():
    mainw = tk.Tk()
    mainw.title("Delete book")
    mainw.geometry("350x150")
    mainw.resizable(False, False)

    frame = tk.Frame(mainw)
    frame.pack(fill='both')

    tk.Label(frame, text="Are you sure you want to delete this book?").pack(pady=(30, 10))
    tk.Button(frame, text="Yes", width=15, command=placeholder).pack(side='left', padx=30, pady=10)
    tk.Button(frame, text="No", width=15, command=placeholder).pack(side='right', padx=30, pady=10)

    mainw.mainloop()


def addWindow():
    mainw = tk.Tk()
    mainw.title("Exercise 3")
    mainw.geometry("300x400")
    mainw.resizable(False, False)

    #-------------------- Variables --------------------
    titl = tk.StringVar()
    auth = tk.StringVar()
    year = tk.IntVar()
    stat = tk.IntVar()

    #-------------------- Window content --------------------
    leftFrame = tk.Frame(mainw, width=200)
    leftFrame.pack(fill='both', expand=True, padx=10, pady=10)

    tk.Label(leftFrame, text="Insert the data of the new book:").pack(pady=(10, 5))
    tk.Label(leftFrame, text="Title:").pack(anchor='center')
    tk.Entry(leftFrame, textvariable=titl, width=40, justify='center').pack(pady=5)
    tk.Label(leftFrame, text="Author:").pack(anchor='center')
    tk.Entry(leftFrame, textvariable=auth, width=40, justify='center').pack(pady=5)
    tk.Label(leftFrame, text="Year:").pack(anchor='center')
    tk.Spinbox(leftFrame, from_=0, to=2025, textvariable=year, justify='center').pack(pady=5)

    tk.Label(leftFrame, text="Status:").pack(anchor='center', pady=5)
    tk.Radiobutton(leftFrame, text="Available", variable=stat, value=1).pack(anchor='w', padx=(100, 0))
    tk.Radiobutton(leftFrame, text="Lend out", variable=stat, value=2).pack(anchor='w', padx=(100, 0))
    tk.Radiobutton(leftFrame, text="Missing", variable=stat, value=3).pack(anchor='w', padx=(100, 0))
    tk.Radiobutton(leftFrame, text="Deleted", variable=stat, value=4).pack(anchor='w', padx=(100, 0))

    tk.Button(leftFrame, text="Add a book", width=20, command=placeholder).pack(pady=(20, 0))

    mainw.mainloop()


def fileOpenWindow():
    mainw = tk.Tk()
    mainw.title("Open a library file")
    mainw.geometry("300x300")
    mainw.resizable(False, False)

    frame = tk.Frame(mainw)
    frame.pack(fill='both', expand=True)

    tk.Label(frame, text="Double-click the library file you want to open:").pack(pady=(20, 10))
    lstb = tk.Listbox(frame)
    lstb.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    lstb.bind('<Double-1>', placeholder)

    mainw.mainloop()


def newFileWindow():
    mainw = tk.Tk()
    mainw.title("Create a new library file")
    mainw.geometry("400x150")
    mainw.resizable(False, False)

    frame = tk.Frame(mainw)
    frame.pack(fill='both', expand=True)

    tk.Label(frame, text="Enter the name of the new library file (no extension needed):").pack(pady=(20, 10))
    tk.Entry(frame, width=40, justify='center').pack(pady=5)
    tk.Button(frame, text="Create", width=20, command=placeholder).pack(pady=10)

    mainw.mainloop()



mainWindow()
#modifyWindow(3)
#deleteWindow()
#addWindow()
#fileOpenWindow()
newFileWindow()