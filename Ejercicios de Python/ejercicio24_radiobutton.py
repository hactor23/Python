from tkinter import *

root = Tk()

varOpcion = IntVar()

def imprimir():
	#print(varOpcion.get())
	if varOpcion.get() == 1:
		etiqueta.config(text = "Has elegido Masculino")
	else:
		etiqueta.config(text = "Has elegido Femenino")

Label(root, text = "Género:").pack()

Radiobutton(root, text = "Hombre", variable = varOpcion, value = 1, command = imprimir).pack()
Radiobutton(root, text = "Mujer", variable = varOpcion, value = 2, command = imprimir).pack()

etiqueta = Label(root)
etiqueta.pack()


root.mainloop()