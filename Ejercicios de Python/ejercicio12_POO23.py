class Persona():

	def __init__(self, nombre, edad, lug_residencia):
		self.nombre = nombre
		self.edad = edad
		self.lug_residencia = lug_residencia

	def descripcion(self):
		print("Nombre: ", self.nombre, " Edad: ", self.edad, " Residencia: ", self.lug_residencia)

class Empleado(Persona):
	def __init__(self, salario, antiguedad, nombre_empleado, edad_empleado, residencia_empleado):
		super().__init__(nombre_empleado, edad_empleado, residencia_empleado) # constructor con parametros para la clase padre...
		self.salario = salario
		self.antiguedad = antiguedad

	def descripcion(self):
		super().descripcion()
		print("Salario: ", self.salario, " Antiguedad: ", self.antiguedad)

#antonio = Persona("Antonio", 55, "España")
#antonio.descripcion()

walter = Empleado(1500, 15, "Walter", 55, "Colombia")
walter.descripcion()

print(isinstance(walter, Empleado)) # verifica si walter es instancia de esta clase...