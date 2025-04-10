import tkinter as tk
import os

def fileOpenWindow(type):
    mainw = tk.Tk()
    mainw.title("Open an existing file")
    mainw.geometry("300x300")
    mainw.resizable(False, False)
    frame = tk.Frame(mainw)
    frame.pack(fill='both', expand=True)
    tk.Label(frame, text="Double-click the file you want to open:").pack(pady=(20, 10))
    lstb = tk.Listbox(frame)
    lstb.pack(fill='both', expand=True, padx=20, pady=(0, 20))
    lstb.bind('<Double-1>', lambda event: [print(lstb.get(lstb.curselection())), mainw.destroy()])                      # here this value should be passed back 

    for file in os.listdir("."):
        if type == 1:
            if file.endswith(".json"):
                lstb.insert('end', file)
        else:
            if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg"):
                lstb.insert('end', file)
    mainw.mainloop()