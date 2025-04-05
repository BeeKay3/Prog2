import tkinter as tk



def mainWindow():
    mainw = tk.Tk()
    mainw.title("Exercise 3")
    mainw.geometry("1200x400")
    mainw.minsize(width=800, height=400)
    mainw.grid_columnconfigure(1, weight=1)
    mainw.grid_rowconfigure(0, weight=1)

    leftFrame = tk.Frame(mainw, width=200)
    leftFrame.grid(row=0, column=0, sticky='ns')

    rightFrame = tk.Frame(mainw, width=1000)
    rightFrame.grid(row=0, column=1, sticky='nsew')
    rightFrame.grid_columnconfigure(0, weight=1)
    rightFrame.grid_rowconfigure(0, weight=1)


    titl = tk.StringVar()
    auth = tk.StringVar()
    year = tk.IntVar()
    avlb = tk.IntVar()
    lend = tk.IntVar()
    miss = tk.IntVar()
    dltd = tk.IntVar()

    tk.Label(leftFrame, text="Title: ").grid(row=0, column=0, padx=10, pady=(20, 0))
    tk.Entry(leftFrame, textvariable=titl, width=40, justify='center').grid(row=1, column=0, padx=10, pady=(0, 10))
    tk.Label(leftFrame, text="Author: ").grid(row=2, column=0, padx=10, pady=(10, 0))
    tk.Entry(leftFrame, textvariable=auth, width=40, justify='center').grid(row=3, column=0, padx=10, pady=(0, 10))
    tk.Label(leftFrame, text="Year: ").grid(row=4, column=0, padx=10, pady=(10, 0))
    tk.Spinbox(leftFrame, from_=0, to=2025, textvariable=year, justify='center').grid(row=5, column=0, padx=10, pady=(0, 10))

    tk.Checkbutton(leftFrame, text="Available", variable=avlb).grid(row=6, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Lend out", variable=lend,).grid(row=7, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Missing", variable=miss).grid(row=8, column=0, sticky='w', padx=(100, 0), pady=0)
    tk.Checkbutton(leftFrame, text="Deleted", variable=dltd).grid(row=9, column=0, sticky='w', padx=(100, 0), pady=0)

    tk.Button(leftFrame, text="Search", width=20).grid(row=10, column=0, padx=10, pady=(10, 0))
    tk.Button(leftFrame, text="Add 1 million books", width=20).grid(row=11, column=0, padx=10, pady=(10, 0))

    lstb = tk.Listbox(rightFrame).grid(row=0, column=0, padx=10, pady=10, sticky='nsew')


    mainw.mainloop()



mainWindow()