import sqlite3

miConexion = sqlite3.connect("GestionProductos")
miCursor = miConexion.cursor()

miCursor.execute("SELECT * FROM PRODUCTOS WHERE SECCION = 'Juguetería' ")
productos = miCursor.fetchall()
print(productos)

#miCursor.execute("UPDATE PRODUCTOS SET PRECIO = 32 WHERE NOMBRE_ARTICULO = 'Pelota' ")
#miCursor.execute("DELETE FROM PRODUCTOS WHERE CODIGO_ARTICULO = 'AR04' ")


miConexion.commit()

miConexion.close()