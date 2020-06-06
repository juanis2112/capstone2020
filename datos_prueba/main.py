# -*- coding: utf-8 -*-
#class Estudiante:
#    def __init__(self,info):
#        # infoe es una lista con la informacion del estudiante
#        # El ultimo atributo es una lista de asignaturas que esta viendo
#        # con esa lista se crea un diccionario (materia,(info_materia))
#        self.doc_ingreso = info[0]
#        self.doc_actual = info[1]
#        self.doc
        
# Informacion para 10 perfiles
import random


# Generamos una lista de documentos de ingreso
doc_ingreso = ["0000","1111","2222","3333","4444",
               "5555","6666","7777","8888","9999"]
# Para la prueba asumimos que son iguales
doc_actual = doc_ingreso
codigo = ["00","01","02","03","04","05","06","07","08","09"]

apellido1 = ["Arevalo","Arango","Diaz","Durán","Martinez",
             "Peña","Gutierrez","Ramos","Naranjo","Torres"]
apellido2 = ["Sanchez","Perez","Guzman","Cortes","Buitrago",
             "Sandoval","Saad","Duque","Cáceres","Castro"]
nombre = ["Andrea","Alfonso","Daniel","Felipe","Natalia",
          "Nicolás","Sofía","Antonia","Isabella","Michael"]

accesos = ["Nuevo al programa","Extranjero","Doble Programa",
                    "Reingreso por Fortalecimiento académico","Terminó condición doble programa",
                    "Nuevo al programa","Nuevo al programa","Nuevo al programa","Nuevo al programa",
                    "Nuevo al programa"]

subaccesos = ["Bachillerato con Examen de Estado", "SER PILO PAGA 4",
              "Departamento de Admisiones", "Generación E","SER PILO PAGA 3",
              "GENERAL","GENERAL","GENERAL","GENERAL","GENERAL"]
correo = []
for i in range(10):
    c = apellido1[i].lower() + "." + nombre[i].lower()+"@urosario.edu.co"
    correo.append(c)
    
sexo = ["M","H","H","H","M","H","M","M","H"]
facultad = ["EICT","EICT","EICT","EICT","EICT",
            "EICT","EICT","EICT","EICT","EICT"]
programa = ["MACC","MACC","MACC","MACC","MACC",
            "MACC","MACC","MACC","MACC","MACC"]

semestre = [6,5,5,4,4,3,2,2,1,1]

