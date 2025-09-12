miDiccionario = {"Alemania":"Berlín", "Francia":"Paris", "España":"Madrid"}
print(miDiccionario)
print(miDiccionario["Francia"])
miDiccionario["Francia"] = "Lisboa"
print(miDiccionario)
del miDiccionario["Francia"]
print(miDiccionario)

miTupla = ["Alemania", "Francia", "España"]
miDiccionario2 = {miTupla[0]:"Berlín", miTupla[1]:"Paris", miTupla[2]:"Madrid"}
print(miDiccionario2)
print(miDiccionario2["Francia"])

miDiccionario3 = {23:"Jordan", "Nombre":"Michael", "Anillos":[1991, 1992, 1994]}
print(miDiccionario3)

miDiccionario32 = {23:"Jordan", "Nombre":"Michael", "Anillos":{"Temporadas":[1991, 1992, 1994]}} #diccionario dentro de diccionario..
print(miDiccionario32["Anillos"])

print(miDiccionario.keys())
print(miDiccionario.values())
print(len(miDiccionario))


