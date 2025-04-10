import tkinter as tk
from PIL import Image, ImageTk
import pyocr
import pyocr.builders

class ImageDrawer:
    def __init__(self, image_path):
        mainw = tk.Tk()
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
            self.text_label.config(text=f"Recognized Text: {recognized_text.strip()}")                                           # here this value should be passed back 
