import math

i = 0

while i <= 10:
	print(i)
	i += 1

edad = int(input("Ingrese edad: "))

while edad < 5 or edad > 100:
	print("Edad incorrecta")
	edad = int(input("Ingrese edad: "))

print("Edad: " + str(edad))


print("Calcula Raiz!!")
numero = int(input("Ingrese número: "))

intentos = 0

while numero < 0:
	print("Ingrese un numero positivo")

	if intentos == 2:
		print("Has usado todos los intentos")
		break; #rompe el bucle...

	numero = int(input("Ingrese número: "))

	if numero < 0:
		intentos += 1

if intentos < 2:
	solucion = math.sqrt(numero)
	print("Raiz cuadrada de " + str(numero) + " es " + str(solucion))
