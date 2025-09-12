def divide():

	try:
		op1 = (float(input("Ingrese un número: ")))
		op2 = (float(input("Ingrese otro número: ")))

		print("La división es: " + str(op1 / op2))

	except ValueError:
		print("Valor Erroneo...")

	except ZeroDivisionError:
		print("Valor no debe ser cero...")

	finally: 		# hace q ocurra si o si las siguientes lineas...
		print("Fin")

divide()
