from tkinter import *

root = Tk()

miFrame = Frame(root, width = 500, height = 400)
miFrame.pack()

miImagen = PhotoImage(file = "alas.png")
#miImagen = PhotoImage(file = "yoda.png")
#miLabel = Label(miFrame, text = "Hola Python")
#miLabel.pack()
#$miLabel.place(x = 100, y = 200)
#Label(miFrame, text = "Hola Amigos!!!", fg = "red", font = ("Comic Sans MS", 23)).place(x = 100, y = 200) #foreground = color texto
Label(miFrame, image = miImagen).place(x =100, y = 200)

root.mainloop()