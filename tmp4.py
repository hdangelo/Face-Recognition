from tkinter import *
root = Tk()
def hello(event): 
    print ('Got tag event')

text = Text()
text.config(font=('courier', 15, 'normal'))            
text.config(width=20, height=12)
text.pack(expand=YES, fill=BOTH)
text.insert(END, 'Lin 1\n\nLin 2\n\nLin 3.\n\n')  

root.mainloop()