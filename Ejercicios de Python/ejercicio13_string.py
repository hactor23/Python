nombre = input("Ingrese nombre: ")
print("El nombre es: ", nombre.upper())
print("El nombre es: ", nombre.lower())
print("El nombre es: ", nombre.capitalize()) # primer letra mayuscula

#print(edad.isdigit())
edad = input("Ingrese edad: ")

while (edad.isdigit() == False):
	edad = input("Ingrese edad: ")

if (int(edad) < 18):
	print("No puede pasar.")
else:
	print("Puede pasasr.")
