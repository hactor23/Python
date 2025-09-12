class Coche():
	def desplazamiento(self):
		print("Me desplazo usando 4 ruedas")


class Moto():
	def desplazamiento(self):
		print("Me desplazo usando 2 ruedas")

class Camion():
	def desplazamiento(self):
		print("Me desplazo usando 8 ruedas")		


miVehiculo = Moto()
miVehiculo.desplazamiento()
miVehiculo2 = Coche()
miVehiculo2.desplazamiento()

def desplazamientoVehiculo(vehiculo): # POLIMORFISMO	
	vehiculo.desplazamiento()

miVehiculo5 = Camion()
desplazamientoVehiculo(miVehiculo5)