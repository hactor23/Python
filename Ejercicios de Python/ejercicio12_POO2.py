# ------------------------------ Clase Padre ------------------------------

class Vehiculos():

	def __init__(self, marca, modelo): # constructor

		self.marca = marca
		self.modelo = modelo
		self.enMarcha = False
		self.acelera = False
		self.frena = False

	def arrancar(self):
		self.enMarcha = True

	def acelerar(self):
		self.acelera = True

	def frenar(self):
		self.frena = True

	def estado(self):
		print("Marca: ", self.marca, "\nModelo: ",
			self.modelo, "\nEn Marcha: ", self.enMarcha, 
			"\nAcelerando: ", self.acelera, "\nFrenando: ", self.frena)


# ------------------------------- Clases Hijas ----------------------------------


class Furgoneta(Vehiculos):

	def carga(self, cargar):
		self.cargado = cargar
		if (self.cargado):
			return "La furgoneta está cargada"
		else:
			return "La furgoneta NO está cargada"


class Moto(Vehiculos):
	hCaballito = ""
	def caballito(self):
		self.hCaballito = "Haciendo caballito"

	def estado(self):
		print("Marca: ", self.marca, "\nModelo: ",
			self.modelo, "\nEn Marcha: ", self.enMarcha, 
			"\nAcelerando: ", self.acelera, "\nFrenando: ", self.frena, "\n", self.hCaballito)


class VElectricos(Vehiculos):
	def __init__(self, marca, modelo):
		super().__init__(marca, modelo)
		self.autonomia = 100

	def cargarEnergia(self):
		self. cargando = True

# ------------------------- Objetos -----------------------------

miMoto = Moto("Honda", "CBR")
miMoto.caballito()
miMoto.estado()

miFurgo = Furgoneta("Renault", "Kangoo")
miFurgo.arrancar()
miFurgo.estado()
print(miFurgo.carga(True))


class BicicletaElectrica(VElectricos, Vehiculos): # se le da preferencia a la clase heredada de la izquierda 
	pass


miBici = BicicletaElectrica("Rubi", "obi")
miBici.estado()

