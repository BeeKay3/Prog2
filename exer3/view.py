import tkinter as tk



def placeholder(variable=None):
    print("Placeholder used! Implement me >:(")


def mainWindow():
    mainw = tk.Tk()
    mainw.title("Exercise 3")
    mainw.geometry("960x480")
    mainw.minsize(width=960, height=480)
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

    tk.Label(leftFrame, text="Fields for searching a book:").grid(row=0, column=0, padx=10, pady=(20, 0))
    tk.Label(leftFrame, text="Title: ").grid(row=1, column=0, padx=10, pady=(10, 0))
    tk.Entry(leftFrame, textvariable=titl, width=40, justify='center').grid(row=2, column=0, padx=10, pady=(0, 10))
    tk.Label(leftFrame, text="Author: ").grid(row=3, column=0, padx=10, pady=(10, 0))
    tk.Entry(leftFrame, textvariable=auth, width=40, justify='center').grid(row=4, column=0, padx=10, pady=(0, 10))
    tk.Label(leftFrame, text="Year: ").grid(row=5, column=0, padx=10, pady=(10, 0))
    tk.Spinbox(leftFrame, from_=0, to=2025, textvariable=year, justify='center').grid(row=6, column=0, padx=10, pady=(0, 10))

    tk.Checkbutton(leftFrame, text="Available", variable=avlb).grid(row=7, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Lend out", variable=lend,).grid(row=8, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Missing", variable=miss).grid(row=9, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Deleted", variable=dltd).grid(row=10, column=0, sticky='w', padx=(100, 0), pady=0)

    tk.Button(leftFrame, text="Search", width=20, command=placeholder).grid(row=11, column=0, padx=10, pady=(10, 0))
    tk.Button(leftFrame, text="Add a book", width=20, command=placeholder).grid(row=12, column=0, padx=10, pady=(30, 0))
    tk.Button(leftFrame, text="Add 1 million books", width=20, command=placeholder).grid(row=13, column=0, padx=10, pady=(10, 0))

    tk.Label(rightFrame, text=f"Library: xxx\nTotal number of books: xxx", font=("Helvetica", 12), height=2, justify='left').grid(row=0, column=0, padx=10, pady=(20, 0), sticky='w')
    lstb = tk.Listbox(rightFrame, font=("Helvetica", 14))
    lstb.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    lstb.bind('<Double-1>', placeholder)
    lstb.bind('<Button-3>', placeholder)
    tk.Label(rightFrame, text=f"To modify a record double-click on it\nTo delete a record right-click on it", height=2, justify='left').grid(row=2, column=0, padx=10, pady=(0, 30), sticky='w')

    for i in range(100):
        lstb.insert(i, f"Book {i + 1}")

    mainw.mainloop()



mainWindow()