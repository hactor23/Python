def devuelve_ciudades(*ciudades): # el asterisco indica q va a ser un numero indefinido de parametros en forma de tuple...
	#for elemento in ciudades:
	#	yield elemento
	for elemento in ciudades:
		#for subElemento in elemento:
			#yield subElemento
		yield from elemento
	

ciudades_devueltas = devuelve_ciudades("Madrid", "Barcelona", "Paris")

print(next(ciudades_devueltas))
print(next(ciudades_devueltas))