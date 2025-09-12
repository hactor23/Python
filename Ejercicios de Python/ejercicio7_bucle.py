for i in [1,2,3]:
	print("Hola")

for i in ["DO", "RE", "MI"]:
	print(i)

for i in ["DO", "RE", "MI"]:
	print("Hola", end = "  ") #acá no hace slato de linea...

email = False

for i in "joj@gmail.com":
	if (i == "@"):
		email = True

if email:
	print("Email correcto")
else:
	print("Email NO correcto")

for i in range(5):
	print(i)

for i in range(5):
	print(f"variable: {i}") # f concatena la variable i con una cadena

for i in range(5, 50, 3): # de 5 a 49 de 3 en 3...
	print(f"variablesss: {i}")

print(len("juan"))

valido = False

email = input("Ingrese email: ")

for i in range(len(email)):
	if email[i] == "@":
		valido = True

if valido:
	print("email valido")
else:
	print("email NO valido")
