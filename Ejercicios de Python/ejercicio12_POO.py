class Coche():

	def __init__(self):		# constructor
		self.__largoChasis = 250
		self.__anchoChasis = 250
		self.__ruedas = 4    # con __ se encapsula la variable...
		self.__enMarcha = False

	def arrancar(self, arrancamos):		
		self.__enMarcha = arrancamos
		if (self.__enMarcha):
			chequeo = self.__chequeo()

		if (self.__enMarcha and chequeo):
			return "El coche está en marcha"
		elif(self.__enMarcha and chequeo == False):
			return "Algo ha ido mal en el chequeo"
		else:
			return "El coche está parado"
 
	def estado(self):
		print("El coche tiene: ", self.__ruedas, " ruedas. Un ancho de ", self.__anchoChasis, " y un largo de ",
			self.__largoChasis, ".")

	def __chequeo(self): # __ encapsula los metodos...
		print("Realizando chequeo...")
		self.gasolina = "oki"
		self.aceite = "ok"
		#self.aceite = "mal"
		self.puertas = "cerradas"

		if (self.gasolina == "oki" and self.aceite == "ok" and self.puertas == "cerradas"):
			return True
		else:
			return False


miCoche = Coche()
#print("El largo del coche es: ", miCoche.largoChasis)
#print("El coche tiene: ", miCoche.ruedas, "ruedas")
print(miCoche.arrancar(True))

miCoche.ruedas = 2 # como está encapsulado no se modifica este atributo
miCoche.estado()

miCoche2 = Coche()
print(miCoche2.arrancar(False))
miCoche2.estado()