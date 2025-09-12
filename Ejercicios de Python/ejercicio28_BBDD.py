import sqlite3

miConexion = sqlite3.connect("PrimeraBase")

miCursor = miConexion.cursor()
#miCursor.execute("CREATE TABLE PRODUCTOS (NOMBRE_ARTICULO VARCHAR(50), PRECIO INTEGER, SECCION VARCHAR(20))") #acá creamos la tabla
#miCursor.execute("INSERT INTO PRODUCTOS VALUES('BALON', 15, 'DEPORTES')") #acá insertamos un objeto de la tabla productos

""" variosProductos = [
	("Camiseta", 10, "Deportes"),
	("Jarrón", 90, "Cerámica"),
	("Camión", 30, "Jufuetería")
]

miCursor.executemany("INSERT INTO PRODUCTOS VALUES (?,?,?)", variosProductos) """

miCursor.execute("SELECT * FROM PRODUCTOS")
variosProductos = miCursor.fetchall()

for p in variosProductos:
	#print(p)
	print("Nombre: ", p[0], "y Sección: ", p[2])

miConexion.commit()



miConexion.close()