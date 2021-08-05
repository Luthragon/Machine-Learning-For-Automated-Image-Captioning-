#!/usr/bin/env python3

"""
ZetCode Tkinter tutorial

In this script, we use the pack manager
to position two buttons in the
bottom-right corner of the window.

Author: Jan Bodnar
Website: www.zetcode.com
"""

from tkinter import *
from tkinter.ttk import Frame, Button, Style

class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Buttons")
        self.style = Style()
        self.style.theme_use("default")

        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, expand=True)

        self.pack(fill=BOTH, expand=True)

        imageBox = Frame(self, width = 200, highlightbackground='grey',highlightthickness=3)
        imageBox.pack(side=LEFT,padx=290,pady=20,ipadx=210,ipady=195)

        closeButton = Button(self, text="EXIT PROGRAM")
        closeButton.pack(side=RIGHT, padx=10, pady=5)
        okButton = Button(self, text="CHOOSE FILE")
        okButton.pack(side=LEFT, padx=10)


def main():

    root = Tk()
    # root.geometry("300x200+300+300")
    root.geometry('1200x800')
    # root.geometry('1920x1080')
    root.resizable(0,0)
    root.title('Caption Generator')
    root.configure(background='#fffbde')
    label=Label(root, font=('arial',15))
    app = Example()
    root.mainloop()


if __name__ == '__main__':
    main()