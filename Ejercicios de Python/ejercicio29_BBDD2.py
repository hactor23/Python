import sqlite3

miConexion = sqlite3.connect("GestionProductos")
miCursor = miConexion.cursor()

#''' para cuando la instruccion es muy larga y uso varios renglones
#miCursor.execute('''
#	CREATE TABLE PRODUCTOS (
#	CODIGO_ARTICULO VARCHAR(4) PRIMARY KEY,
#	NOMBRE_ARTICULO VARCHAR(50),
#	PRECIO INTEGER,
#	SECCION VARCHAR(20)
#	)
#	''')

#miCursor.execute('''
#	CREATE TABLE PRODUCTOS_2 (
#	ID INTEGER PRIMARY KEY AUTOINCREMENT,
#	NOMBRE_ARTICULO VARCHAR(50),
#	PRECIO INTEGER,
#	SECCION VARCHAR(20)
#	)
#	''')

'''productos = [
	("AR01", "Pelota", 20, "Juguetería"),
	("AR02", "Pantalón", 15, "Confección"),
	("AR03", "Tornillo", 2, "Ferretería"),
	("AR04", "Jarrón", 32, "Cerámica")
]'''

miCursor.execute('''
	CREATE TABLE PRODUCTOS_23 (
	ID INTEGER PRIMARY KEY AUTOINCREMENT,
	NOMBRE_ARTICULO VARCHAR(50) UNIQUE,
	PRECIO INTEGER,
	SECCION VARCHAR(20)
	)
	''')

productos = [
	("Pelota", 20, "Juguetería"),
	("Pantalón", 15, "Confección"),
	("Tornillo", 2, "Ferretería"),
	("Jarrón", 32, "Cerámica")
]

miCursor.executemany("INSERT INTO PRODUCTOS_23 VALUES (NULL, ?,?,?)", productos)


miConexion.commit()

miConexion.close()