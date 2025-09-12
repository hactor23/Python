miTupla = ("Juan", 13, 1 , 1995, 13)
miLista = list(miTupla) #convierte una tupla en una lista...
print(miTupla[1])
print(miLista)
print(miTupla)
miTupla2 = tuple(miLista) #convierte una lista en una tupla...
print(miTupla2)
print("Juan" in miTupla)
print(miTupla.count(13)) #cuenta cuantas veces está un elemento
print(len(miTupla)) #cuenta elementos de una tupla
miTupla3 = "John", 23, 5
print(miTupla3)

nombre, dia, mes = miTupla3 #desempaqutado de tuplas...
print(nombre)