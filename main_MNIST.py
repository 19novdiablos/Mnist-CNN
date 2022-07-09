import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import PIL
import numpy
import cv2
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk, ImageDraw, ImageOps
import tkinter.filedialog as fd
import tensorflow as tf

#Loadmodel
# model = tf.keras.models.load_model(r'E:\Study\NoronNhanTao\MODEL\CNN_Mnist.model')
model = tf.keras.models.load_model('E:/Study/NoronNhanTao/MODEL/CNN_Mnist.model')

#Predict
def predict(name):
    img_pred = cv2.imread(name)
    img_pred = cv2.cvtColor(img_pred, cv2.COLOR_BGR2GRAY)
    img_pred = cv2.resize(img_pred, (28, 28))
    img_pred = tf.keras.utils.img_to_array(img_pred)
    img_pred = img_pred.reshape(1, 28, 28)
    pred_main = model.predict(img_pred).argmax(axis=1)
    return pred_main

def New_Window():
    def paint(event):
        x1, y1 = (event.x - 5), (event.y - 5)
        x2, y2 = (event.x + 5), (event.y + 5)
        canvas.create_oval((x1, y1, x2, y2), fill='white', width=10)
        #  --- PIL
        draw.line((x1, y1, x2, y2), fill='white', width=10)
    Window = tk.Toplevel()
    Window.title("Paint Application")
    canvas = tk.Canvas(Window, height=300, width=300)
    canvas.bind('<B1-Motion>', paint)
    canvas.pack()

    pil_image = PIL.Image.new('RGB', (300, 300), 'black')
    draw = ImageDraw.Draw(pil_image)

    def clearAll():
        canvas.delete("all")
        lbl.config(image="")
        lbl_pred.config(text="")
        Window.destroy()

    def ok():
        img = pil_image
        resized = img.resize((230, 250))
        img = ImageTk.PhotoImage(resized)
        lbl.configure(image=img)
        lbl.image = img

        img1 = pil_image
        img_pred = img1.resize((28, 28))
        img_pred = ImageOps.grayscale(img_pred)
        img_pred = tf.keras.utils.img_to_array(img_pred)
        img_pred = img_pred.reshape(1, 28, 28)
        pred_main = model.predict(img_pred).argmax(axis=1)
        lbl_pred.configure(text=pred_main)

        Window.destroy()

    frm1 = Frame(Window)
    frm1.pack(side=BOTTOM, padx=15, pady=15)
    btn_ok = Button(frm1, text="OK", command=lambda: ok())
    btn_ok.pack(side=tk.LEFT, padx=10, pady=10)
    btn_clear = Button(frm1, text="Close", command=lambda: clearAll())
    btn_clear.pack(padx=10, pady=10)


# Lấy ảnh từ máy tính.
def showImage():
    global img
    name = fd.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=(("JPG File", "*.png"),("All Files", "*.*")))
    print(name)
    img = Image.open(name)
    resized = img.resize((230, 250))
    img = ImageTk.PhotoImage(resized)
    lbl.configure(image=img)
    lbl.image = img

    pred = predict(name)
    lbl_pred.configure(text=pred)

#Thiết kế giao diện
window = tk.Tk()
window.title('PHẠM HOÀNG HIỆP')
window.geometry("400x450")
greeting = tk.Label(window,text="Nhận Diện Số Viết Tay", font=('calibri', 20, 'bold'))
greeting.pack()

style = Style()
style.configure('TButton', font=('calibri', 10, 'bold'), borderwidth='4')
style.map('TButton', foreground=[('active', '!disabled', 'blue')], background=[('active', 'black')])

lbl = Label(window)
lbl.pack(padx=15, pady=15)


frm = Frame(window)
frm.pack(side=BOTTOM, padx=15, pady=15)
btn = Button(frm, text="Open File", command=showImage)
btn.pack(side=tk.LEFT,padx=10, pady=10)
btn1 = Button(frm, text="Open Paint", command=lambda: New_Window())
btn1.pack(side=tk.LEFT,padx=10, pady=10)
btn2 = Button(frm, text="Exit", command=lambda: exit())
btn2.pack(padx=10, pady=10)

frm_pred = Frame(window)
frm_pred.pack(side=BOTTOM)
lbl2 = Label(frm_pred, text='Predict is: ',font=('Arial', 13))
lbl2.pack(side=LEFT, padx=10, pady=10)
lbl_pred = Label(frm_pred,font=('Arial', 13))
lbl_pred.pack(padx=10, pady=10)

window.mainloop()