from tkinter import *

root = Tk()

root.title("Ejemplo")

playa = IntVar()
montgna = IntVar()
turismo = IntVar()

def opcionesViaje():
	opcionElegida = ""
	if (playa.get() == 1):
		opcionElegida += " playa"
	if (montgna.get() == 1):
		opcionElegida += " montaña"
	if (turismo.get() == 1):
		opcionElegida += " turismo"
	
	textoFinal.config(text = opcionElegida)

foto = PhotoImage(file = "alas.png")
Label(root, image = foto).pack()

frame = Frame(root)
frame.pack()

Label(frame, text = "Elige destinos", width = 50).pack()

Checkbutton(root, text = "Playa", variable = playa, onvalue = 1, offvalue = 0, command = opcionesViaje).pack()
Checkbutton(root, text = "Montaña", variable = montgna, onvalue = 1, offvalue = 0, command = opcionesViaje).pack()
Checkbutton(root, text = "Turismo", variable = turismo, onvalue = 1, offvalue = 0, command = opcionesViaje).pack()


textoFinal = Label(frame)
textoFinal.pack()

root.mainloop()