from tkinter import*

master = Tk()
var = IntVar()
Label(master, text = "Select OCR language").grid(row=0, sticky=W)
Radiobutton(master, text = "default", variable = var, value = 1).grid(row=1, sticky=W)
Radiobutton(master, text = "user-defined", variable = var, value = 2).grid(row=2, sticky=W)
Button(master, text = "OK", command = master.quit).grid(row=3, sticky=W)
selection = var.get()
print ("Selection:", selection)
mainloop()