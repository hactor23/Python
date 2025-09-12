""" def area_triangulo(base, altura):
	return (base * altura) / 2

#print(area_triangulo(5, 7))
triangulo1 = area_triangulo(5,7)
triangulo2 = area_triangulo(9,6)
triangulo3 = area_triangulo(2,3)

print(triangulo1)
print(triangulo2) """

area_triangulo = lambda base, altura : (base * altura) / 2

print(area_triangulo(7, 5))
print(area_triangulo(9,6))

#al_cubo = lambda numero : pow(numero, 3)
al_cubo = lambda numero : numero ** 3

print(al_cubo(5))


destacar_valor = lambda comision : "¡{}! €".format(comision)

comision_ana = 15585

print(destacar_valor(comision_ana))

