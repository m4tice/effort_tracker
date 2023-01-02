# pylint: skip-file

import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_153=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        GLabel_153["font"] = ft
        GLabel_153["fg"] = "#333333"
        GLabel_153["justify"] = "center"
        GLabel_153["text"] = "label"
        GLabel_153.place(x=330,y=20,width=70,height=25)

        GButton_785=tk.Button(root)
        GButton_785["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_785["font"] = ft
        GButton_785["fg"] = "#000000"
        GButton_785["justify"] = "center"
        GButton_785["text"] = "Button"
        GButton_785.place(x=130,y=70,width=70,height=25)
        GButton_785["command"] = self.GButton_785_command

        GButton_273=tk.Button(root)
        GButton_273["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_273["font"] = ft
        GButton_273["fg"] = "#000000"
        GButton_273["justify"] = "center"
        GButton_273["text"] = "Button"
        GButton_273.place(x=30,y=70,width=70,height=25)
        GButton_273["command"] = self.GButton_273_command

        GButton_945=tk.Button(root)
        GButton_945["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_945["font"] = ft
        GButton_945["fg"] = "#000000"
        GButton_945["justify"] = "center"
        GButton_945["text"] = "Button"
        GButton_945.place(x=230,y=70,width=70,height=25)
        GButton_945["command"] = self.GButton_945_command

        GButton_369=tk.Button(root)
        GButton_369["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_369["font"] = ft
        GButton_369["fg"] = "#000000"
        GButton_369["justify"] = "center"
        GButton_369["text"] = "Button"
        GButton_369.place(x=330,y=70,width=70,height=25)
        GButton_369["command"] = self.GButton_369_command

    def GButton_785_command(self):
        print("command")


    def GButton_273_command(self):
        print("command")


    def GButton_945_command(self):
        print("command")


    def GButton_369_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
