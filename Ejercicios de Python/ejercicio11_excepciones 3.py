import math

def calculaRaiz(num1):
	if num1 < 0:
		raise ValueError ("El número no debe ser negativo")
	else:
		return math.sqrt(num1)

op1 = (int(input("Ingrese un número: ")))

try:
	print(calculaRaiz(op1))
except ValueError as ErrorDeNegativo:
	print(ErrorDeNegativo)

print("Fin...")




def evaluaEdad(edad):

	if edad < 0:
		raise TypeError("No se permiten edades negativas")
		#raise ZeroDivisionError("No se permiten edades negativas")
		#raise MiPropioError("No se permiten edades negativas")

	if edad < 20:
		return "eres muy joven"
	elif edad < 40:
		return "eres joven"
	elif edad < 65:
		return "eres maduro"
	elif edad < 100:
		return "cuidate..."

print(evaluaEdad(15))