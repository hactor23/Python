from tkinter import *
from tkinter import filedialog

root = Tk()

def abrirFichero():
	#fichero = filedialog.askopenfilename(title = "Abrir")
	fichero = filedialog.askopenfilename(title = "Abrir", initialdir = "C:", filetypes = (("Fichero de Escel", "*.xlsx"),
		("Ficheros de Texto", "*.txt")))
	print (fichero)	

Button(root, text = "Abrir fichero", command = abrirFichero).pack()


root.mainloop()