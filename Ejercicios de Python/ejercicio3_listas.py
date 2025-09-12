miLista = ["A", "B", "C", "D", "E"]

print(miLista[2])

print(miLista[0:3]) # desde el elemento 0, inclusive, hasta el elemento 2

print(miLista[:3]) # mismo q la linea d arriba

print(miLista[2:])

print(miLista[:])

miLista.append("Sandra")

print(miLista)

miLista.insert(3, "Luck")

print(miLista)

miLista.extend(["x", "y", "z"])

print(miLista)

print(miLista.index("x"))

print("z" in miLista)

miLista.append(23)

print(miLista)

miLista.remove(23)

print(miLista)

miLista.pop() #elimina el último elemento de la lista

print(miLista)

miLista2 = [32, 55, "lol"]

miLista3 = miLista + miLista2

print(miLista3)