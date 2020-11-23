import cv2
import PIL
import numpy
import pytesseract
from PIL import Image,ImageTk
from tkinter import *
from tkinter import ttk,messagebox

class GUI:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        self.num1,self.num2=numpy.random.randint(low=0, high=10, size=2)
        self.video=cv2.VideoCapture(0)
        self.win = Tk()
        self.win.title('Sum 4 Kids')
        self.win.configure(background='dark SeaGreen1')
        self.win.geometry("500x600")
        self.win.resizable(width=False, height=False)
        label = Label(self.win,text='Set your answer in red box.',padx=5,pady=5,bd=3,bg='azure',fg='purple',font=("Times", 13, "bold italic"))
        label.place(relx=0.32,rely=0.01)
        self.camera = Label(self.win,padx=10,pady=10,bd=3,bg='blue')
        self.camera.place(relx=0.014,rely=0.08)
        self.FRAME()
        self.GAME()
        self.win.mainloop()
        
    def FRAME(self):
        ret,self.frame=self.video.read()
        self.frame=cv2.resize(self.frame,(480,400))
        cv2.rectangle(self.frame,(120,100),(300,300),(0,0,255),3)
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        imgtk = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        self.camera.imgtk = imgtk
        self.camera.configure(image=imgtk)
        self.camera.after(10, self.FRAME)
        
    def GAME(self):
        number = Label(self.win,text='{} + {} = ?'.format(self.num1,self.num2),padx=5,pady=5,bd=3,bg='yellow',fg='black',font=("Times", 15, "bold"))
        number.place(relx=0.4,rely=0.9)
        guess=cv2.cvtColor(self.frame[100:300,120:360],cv2.COLOR_BGR2GRAY)
        guess=cv2.Laplacian(guess, cv2.CV_8U, 3,3, 2)
        guess= cv2.dilate(guess,(3,3),iterations = 1)
        guess = cv2.morphologyEx(guess, cv2.MORPH_OPEN, (11,11))
        cv2.imshow('box',guess)
        self.result=pytesseract.image_to_string(guess, config=r'--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
        if self.result!='':
            print(self.result)
            result = Label(self.win,text='Your Answer: {}'.format(self.result),padx=5,pady=5,bd=3,bg='yellow',fg='black',font=("Times", 15, "bold"))
            result.place(relx=0.337,rely=0.95)
            if self.num1+self.num2==int(self.result):
                messagebox.showinfo(title='SUM 4 KIDS',message='Your answer is correct...'+'\n'+'try again',parent=self.win,icon='info')
                self.num1,self.num2=numpy.random.randint(low=0, high=10, size=2)
                result = Label(self.win,text='Your Answer: ',padx=5,pady=5,bd=3,bg='yellow',fg='black',font=("Times", 15, "bold"))
        self.win.after(50, self.GAME)           

gui=GUI()
