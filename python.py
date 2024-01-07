from ast import main
import os 
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import sys
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from turtle import width

class PrintLogger(object):  # create file like object

    def __init__(self, textbox):  # pass reference to text widget
        self.textbox = textbox  # keep ref

    def write(self, text):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert("end", text)  # write text to textbox
        self.textbox.see("end")  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def flush(self):  # needed for file like object
        pass

class MyGUI:
    def __init__(self):
        

        self.root = Tk()
        self.root.title("MST")
        self.root.geometry("600x200")
        self.root.resizable(False, False)
        self.address = ''
        self.com = 'COM1'

        self.btnProgram = Button(self.root, text='Erase and Program', command= self.eraseAndProgram, width= 15 , height=1)
        self.btnProgram.place(x= 450, y= 75)

        self.btnProgram = Button(self.root, text='Program', command= self.program, width= 9 , height=1)
        self.btnProgram.place(x=360, y= 75)

        self.btnProgram = Button(self.root, text='Erase', command= self.erase, width= 9 , height=1)
        self.btnProgram.place(x= 270, y= 75)

        self.open_button = Button(self.root, text='Open a File', command=self.select_file)
        self.open_button.place(x = 475, y= 30)

        self.log_widget = ScrolledText(self.root, height=5, width=96, font=("consolas", "8", "normal"))
        self.log_widget.place(y= 120)
        logger = PrintLogger(self.log_widget)
        sys.stdout = logger
        sys.stderr = logger

        self.label = Label( self.root , text= self.address , background= 'white', width= 60 , height = 2, justify= LEFT,)
        self.label.place(x = 20, y= 25)

        self.OPTIONS = [ "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10"] #etc

        self.variable = StringVar(self.root)
        self.variable.set('Com1')

        option_menu = OptionMenu(self.root, self.variable, *self.OPTIONS, command= self.option_menu)
        option_menu.place(x= 20, y= 75)

    def option_menu(self, *args):
        self.com = self.variable.get()
        print(f'{self.com} Selected')
        

    def select_file(self):
        filetypes = (('bin files', '*.bin'),('All files', '*.*'))
        filename = fd.askopenfilename(
            title='Open a file', initialdir='/', filetypes=filetypes)

        self.address = filename
        self.label.config(text=self.address)

    def mloop(self):
        self.root.mainloop()
    
    def eraseAndProgram(self):
        if(self.address == ''):
            print('no file selected')
          
        else:
            cmd = 'esptool -p ' + self.com + ' erase_flash' 
            os.system(cmd)
            cmd = 'esptool -p ' + self.com + ' write_flash 0x0 ' + "\""  + self.address + "\""
            os.system(cmd)
       

    def erase(self):
        cmd = 'esptool -p ' + self.com + ' erase_flash' 
        os.system(cmd)

    def program(self):
        if(self.address == ''):
              print('no file selected')
        else:
            cmd = 'esptool -p ' + self.com + ' write_flash 0x0 ' + "\"" + self.address + "\"" 
            os.system(cmd)
           

def main():
    myGUI = MyGUI()
    myGUI.mloop()

if __name__ == "__main__":
    main()
