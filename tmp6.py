from tkinter import *

class myClass(object):
    def myMethod(self):
        print("Hello World!")

class Application(Frame):
    """ GUI application which can reveal the secret of longevity. """
    def __init__ (self, master):
        super(Application, self).__init__(master)
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        # Create a text box
        self.txtBox = Text(self, width = 300, height = 300, wrap = WORD)
        self.txtBox.grid(row = 0, column = 0, sticky = W)

        # display message
        message = myClass.myMethod
        self.txtBox.insert(0.0, message)

# main
root = Tk()
root.title("My Title")
root.geometry("500x500")

app = Application(root)

root.mainloop()