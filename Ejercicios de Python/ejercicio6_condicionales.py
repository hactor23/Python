print("Evaluación de Notas")
nota_alumno = input("Ingrese nota: ")

def evaluacion(nota):	
	if nota >= 10:
		valor = "Diez"
	elif nota < 6:
		valor = "Suspenso"	
	else:
		valor = "Aprobado"
	return valor

print(evaluacion(int(nota_alumno)))


print("Asignaturas Optativas")
opcion = input("Ingrese asignatura: ")
asignatura = opcion.lower()

if asignatura in ("informatica", "matematica"):
	print("Asignatura: " + asignatura)
else:
	print("No está!!!")