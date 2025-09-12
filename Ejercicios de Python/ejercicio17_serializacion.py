""" import pickle

lista_nombres = ["Pedro", "Ana", "María"]

fichero_binario = open("lista_nombres", "wb") #write binarie - escritura binaria

pickle.dump(lista_nombres, fichero_binario)

fichero_binario.close()

del (fichero_binario) """

import pickle

fichero = open("lista_nombres", "rb")

lista = pickle.load(fichero)

print(lista)