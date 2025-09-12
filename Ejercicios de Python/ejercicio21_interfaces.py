from tkinter import *

raiz = Tk()

miFrame = Frame(raiz, width = 600, height = 600)
miFrame.pack()

miNoombre = StringVar()

cuadroNombre = Entry(miFrame, textvariable = miNoombre)
#cuadroTexto.place(x = 100, y = 100)
cuadroNombre.grid(row = 0, column = 1, padx = 10, pady = 10) # grilla con filas y columnas
cuadroNombre.config(fg = "red", justify = "right")
cuadroApellido = Entry(miFrame)
cuadroApellido.grid(row = 1, column = 1, padx = 10, pady = 10) # grilla con filas y columnas
cuadroPass = Entry(miFrame)
cuadroPass.grid(row = 2, column = 1, padx = 10, pady = 10) # grilla con filas y columnas
cuadroPass.config(show = "*")

textoComentario = Text(miFrame, width = 16, height = 5)
textoComentario.grid(row = 3, column = 1, padx = 10, pady = 10) 

scrollVert = Scrollbar(miFrame, command = textoComentario.yview)
scrollVert.grid(row = 3, column = 2, sticky = "nsew") #nsew es para adaptar la scrollbar

textoComentario.config(yscrollcommand = scrollVert.set)

nombreLabel = Label(miFrame, text = "Nombre: ")
#nombreLabel.place(x = 100, y = 100)
nombreLabel.grid(row = 0, column = 0, sticky = "e", padx = 10, pady = 10) # con sticky alineo a la derecha y pady es la distancia entre elementos
apellidoLabel = Label(miFrame, text = "Apellido: ")
apellidoLabel.grid(row = 1, column = 0, sticky = "e", padx = 10, pady = 10)
passLabel = Label(miFrame, text = "Password: ")
passLabel.grid(row = 2, column = 0, sticky = "e", padx = 10, pady = 10)
comentarioLabel = Label(miFrame, text = "Comentario: ")
comentarioLabel.grid(row = 3, column = 0, sticky = "e", padx = 10, pady = 10)

def codigoBoton():
	miNoombre.set("Juan")

botonEnvio = Button(raiz, text = "Enviar", command = codigoBoton)

botonEnvio.pack()

raiz.mainloop()
