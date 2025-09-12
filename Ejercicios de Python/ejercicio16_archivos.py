from io import open

""" archivo_texto = open("archivo.txt", "w")
frase = "Buen Día!! \nLunes :("
archivo_texto.write(frase)
archivo_texto.close() """

""" archivo_texto = open("archivo.txt", "r")
texto = archivo_texto.read()
archivo_texto.close()
print(texto) """

""" archivo_texto = open("archivo.txt", "r")
lineas_texto = archivo_texto.readlines()
archivo_texto.close()
print(lineas_texto)
print(lineas_texto[0]) """

""" archivo_texto = open("archivo.txt", "a") #append al archivo
archivo_texto.write("\nLuck yo soy tu padre")
archivo_texto.close() """

# seek es el puntero

#archivo_texto = open("archivo.txt", "r")
#print(archivo_texto.read())

#archivo_texto.seek(5)
#print(archivo_texto.read())
#print(archivo_texto.read(5))
#print(len(archivo_texto.read())/2)
#archivo_texto.seek(len(archivo_texto.readline()))
#print(archivo_texto.read())

archivo_texto = open("archivo.txt", "r+") # lectura y escritura
print(archivo_texto.read())
archivo_texto.write("Luck soy tu padre")
print(archivo_texto.read())
archivo_texto.close()

