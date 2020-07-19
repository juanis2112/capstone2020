"""Este archivo contiene todas las funciones necesarias para ejecutar los modelos de Machine Learning y levantar alertas
 de estudiantes. Hay dos grupos de funciones: las que funcionan analizando los cortes 1 y 2 y las funciones que analizan solo
 el corte 1.

@author: Juan Camilo Ruiz
@author: Juan Miguel Gutierrez

"""
#NOTA: Revisar que paquetes son necesarios e importaciones son necesarias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import silhouette_score, confusion_matrix,classification_report,accuracy_score, precision_score
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from scipy.stats import entropy
import pickle



# NOTA: Variable global para modelos. El que quiera debe crear la lista con todos los modelos afuera de la funcion?
lista_modelos =[GaussianNB(),LogisticRegression(),DecisionTreeClassifier(),KNeighborsClassifier(),svm.SVC(kernel='rbf')]
#=======================================================================================================================
# FUNCIONES DE MODELOS PARA SOLO EL PRIMER CORTE


def funcion_paso(x):
    """
    Funcion necesaria para crear la columna Paso en el dataframe.
    
    PARAMETROS:
        x: nota final

    RETORNA: 
        1 si el estudiante paso (x >= 3) o 0 si perdio (x < 3) como etiqueta para modelos de prediccion
    """
    if(x >= 3):
        return 1
    elif(x <3):
        return 0
#-----------------------------------------------------------------------------
def mejor_modelo_general_2(materia):
    """
    Determina el mejor modelo (modelo general sobre todas las materias) sobre todos los datos.
    El analisis es realizado con las notas de los cortes 1 y 2.

    PARAMETROS:
        materia: dataframe con notas en todas las materias

    RETORNA:
        mejor_modelo:  modelo correspondiente al modelo general
        F15_mejor_modelo: el puntaje F15 asociado al modelo general
    """
    X = materia[["Nota_1er_Corte","Nota_2do_Corte"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    mejor_modelo = lista_modelos[0] #Inicializando para eleccion de modelo
    F15_mejor_modelo = 0 # Inicializando puntaje F.15, el cual es el que nos vamos a basar para la elección del modelo
    for i in range(len(lista_modelos)):
        modelo = lista_modelos[i]
        modelo.fit(X_train,Y_train)
        Y_pred = modelo.predict(X_test)
        cm = confusion_matrix(Y_test,Y_pred,labels = [0, 1])
        True_posit=cm[0][0]
        True_neg=cm[1][1]
        False_neg=[1][0]
        False_posit=cm[0][1]
        Total = True_posit+True_neg+False_neg+False_posit
        Accuracy = (True_posit+True_neg)/Total
        Accuracy_pass = (True_neg)/(True_neg+False_posit)
        Accuracy_fail = (True_posit)/(True_posit+False_neg)
        F15=((1+1.5*1.5)*True_posit)/((1+1.5*1.5)*True_posit+(1.5*1.5)*False_neg+False_posit)

        if F15 > F15_mejor_modelo:
            F15_mejor_modelo = F15
            mejor_modelo = modelo

        print(r"F_{1.5}$:" +str(F15))
    return mejor_modelo,F15_mejor_modelo
#------------------------------------------------------------------------------
def mejor_modelo_2(materia,modelo_general):
    """
    Determina el mejor modelo para una materia teniendo en cuenta las clases en las que todos pasaron.
    El analisis es realizado con las notas de los cortes 1 y 2.
    
    PARAMETROS:
        materia: dataframe con los datos de una materia especifica
        modelo_genera: modelo general pre-establecido
     
    RETORNA:
        mejor_modelo: modelo correspondiente al modelo general
        F_15_mejor_modelo: puntaje F15 asociado al modelo general

    """
    X = materia[["Nota_1er_Corte","Nota_2do_Corte"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    if Y_train["Paso"].nunique()==1: # Codigo para saber si solo posee una clase de prediccion o dos
        Y_pred = modelo_general.predict(X_test)
        cm = confusion_matrix(Y_test,Y_pred,labels = [0, 1])
        True_posit=cm[0][0]
        True_neg=cm[1][1]
        False_neg=[1][0]
        False_posit=cm[0][1]
        Total = True_posit+True_neg+False_neg+False_posit
        Accuracy = (True_posit+True_neg)/Total
        Accuracy_pass = (True_neg)/(True_neg+False_posit)
        Accuracy_fail = (True_posit)/(True_posit+False_neg)
        F15=((1+1.5*1.5)*True_posit)/((1+1.5*1.5)*True_posit+(1.5*1.5)*False_neg+False_posit)
        return modelo_general,F15
    else:
        mejor_modelo = lista_modelos[0] #Inicializando para eleccion de modelo
        F15_mejor_modelo = 0 # Inicializando puntaje F.15, el cual es el que nos vamos a basar para la elección del modelo
        for i in range(len(lista_modelos)):
            modelo = lista_modelos[i]
            modelo.fit(X_train,Y_train)
            Y_pred = modelo.predict(X_test)
            cm = confusion_matrix(Y_test,Y_pred,labels = [0, 1])
            True_posit=cm[0][0]
            True_neg=cm[1][1]
            False_neg=[1][0]
            False_posit=cm[0][1]
            Total = True_posit+True_neg+False_neg+False_posit
            Accuracy = (True_posit+True_neg)/Total
            Accuracy_pass = (True_neg)/(True_neg+False_posit)
            Accuracy_fail = (True_posit)/(True_posit+False_neg)
            F15=((1+1.5*1.5)*True_posit)/((1+1.5*1.5)*True_posit+(1.5*1.5)*False_neg+False_posit)

            if F15 > F15_mejor_modelo:
                F15_mejor_modelo = F15
                mejor_modelo = modelo

            #print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------

def seleccionar_guardar_modelo_general_2(materia):
    """
    Guarda el mejor modelo, es decir el modelo general, sobre todas las materias.
    El analisis es realizado con las notas de los cortes 1 y 2.

    PARAMETROS:
        materia: dataframe con las notas de todos las materias de todos los estudiantes
    """
    nombre_materia = "Modelo_General"
    mejor_modelo1,F15 = mejor_modelo_general_2(materia)
    #Guardar el modelo en disco
    filename = "modelos/mejor_modelo_"+nombre_materia+"1,2.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
def seleccionar_guardar_modelo_2(materia,nombre_materia):
    """
    Guarda el mejor modelo sobre una materia específica.
    El analisis es realizado con las notas de los cortes 1 y 2.
    
    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    modelo_general_nombre = "Modelo_General"
    filename = "modelos/mejor_modelo_"+modelo_general_nombre+"1,2.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    mejor_modelo1,F15 = mejor_modelo_2(materia,modelo_general)
    #Guardar el modelo en disco
    filename = "modelos/mejor_modelo_"+nombre_materia+"1,2.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
def cargar_modelo_2(nombre_materia):
    """
    Carga un modelo de prediccion que usa cortes 1 y 2

    PARAMETROS:
        nombre_materia: string del nombre de la materia para cargar el modelo

    RETORNA:
        loaded_model: mejor modelo asociado a la materia elegida
    """
    filename = "modelos/mejor_modelo_"+nombre_materia+"1,2.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
#--------------------------------------------------------------------------------------------------------------------
def guardar_mejor_modelo_todas_materias_2(df_completo):
    """
    Guarda el mejor modelo para todas las materias analizando cortes 1 y 2

    PARAMETROS:
        df_completo: dataframe con los datos de todos los estudiantes
    """
    materias = pd.DataFrame(df_completo.groupby("Nombre_Asignatura")).reset_index()
    lista_materias = []
    for index,row in materias.iterrows():
        lista_materias.append(row[0])
    for i in range(len(lista_materias)):
        nombre_materia = lista_materias[i]
        materia = df_completo[df_completo["Nombre_Asignatura"] == nombre_materia]
        seleccionar_guardar_modelo_2(materia,nombre_materia)
#--------------------------------------------------------------------------------------------------------------------
def devolucion_estudiantes_riesgos_2(nombre_materia,materia):
    """
    Retorna dataframe de estudiantes que el modelo predijo que van a perder

    PARAMETROS:
        nombre_materia: nombre de la materia que selecciona para cargar el modelo (puede ser el nombre del archivo con el modelo general)
        materia: dataframe con los datos de las notas de la materia especificada

    RETORNA:
        estudiantes: dataframe con los estudiantes que se predijo que van a perder la materia
    """
    # NOTA: Los datos en materia corresponden a la tabla de datos del semestre actual para sacar las alertas
    loaded_model = cargar_modelo_2(nombre_materia)
    X_test = materia[["Nota_1er_Corte","Nota_2do_Corte"]]
    Y_pred = loaded_model.predict(X_test)
    Prediccion = X_test
    Prediccion["Pred"]=Y_pred
    idx = Prediccion.index[Prediccion["Pred"]==0]
    estudiantes = materia.loc[idx]
    return estudiantes
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
# FUNCIONES DE MODELOS PARA SOLO EL PRIMER CORTE
def mejor_modelo_general_1(materia):
    """
    Determina el mejor modelo (modelo general sobre todas las materias) sobre todos los datos.
    El analisis es realizado con las notas del corte 1.

    PARAMETROS:
        materia: dataframe con notas en todas las materias

    RETORNA:
        mejor_modelo:  modelo correspondiente al modelo general
        F15_mejor_modelo: el puntaje F15 asociado al modelo general
    """
    X = materia[["Nota_1er_Corte"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    mejor_modelo = lista_modelos[0] #Inicializando para eleccion de modelo
    F15_mejor_modelo = 0 # Inicializando puntaje F.15, el cual es el que nos vamos a basar para la elección del modelo
    for i in range(len(lista_modelos)):
        modelo = lista_modelos[i]
        modelo.fit(X_train,Y_train)
        Y_pred = modelo.predict(X_test)
        cm = confusion_matrix(Y_test,Y_pred,labels = [0, 1])
        True_posit=cm[0][0]
        True_neg=cm[1][1]
        False_neg=[1][0]
        False_posit=cm[0][1]
        Total = True_posit+True_neg+False_neg+False_posit
        Accuracy = (True_posit+True_neg)/Total
        Accuracy_pass = (True_neg)/(True_neg+False_posit)
        Accuracy_fail = (True_posit)/(True_posit+False_neg)
        F15=((1+1.5*1.5)*True_posit)/((1+1.5*1.5)*True_posit+(1.5*1.5)*False_neg+False_posit)

        if F15 > F15_mejor_modelo:
            F15_mejor_modelo = F15
            mejor_modelo = modelo

        print(r"F_{1.5}$:" +str(F15))
    return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------
def mejor_modelo_1(materia,modelo_general):
    """
    Determina el mejor modelo para una materia teniendo en cuenta las clases en las que todos pasaron.
    El analisis es realizado con las notas del corte 1 y 2.
    
    PARAMETROS:
        materia: dataframe con los datos de una materia especifica
        modelo_genera: modelo general pre-establecido
     
    RETORNA:
        mejor_modelo: modelo correspondiente al modelo general
        F_15_mejor_modelo: puntaje F15 asociado al modelo geenral
    """
    X = materia[["Nota_1er_Corte"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    if Y_train["Paso"].nunique()==1: # Codigo para saber si solo posee una clase de prediccion o dos
        Y_pred = modelo_general.predict(X_test)
        cm = confusion_matrix(Y_test,Y_pred,labels = [0, 1])
        True_posit=cm[0][0]
        True_neg=cm[1][1]
        False_neg=[1][0]
        False_posit=cm[0][1]
        Total = True_posit+True_neg+False_neg+False_posit
        Accuracy = (True_posit+True_neg)/Total
        Accuracy_pass = (True_neg)/(True_neg+False_posit)
        Accuracy_fail = (True_posit)/(True_posit+False_neg)
        F15=((1+1.5*1.5)*True_posit)/((1+1.5*1.5)*True_posit+(1.5*1.5)*False_neg+False_posit)
        return modelo_general,F15
    else:
        mejor_modelo = lista_modelos[0] #Inicializando para eleccion de modelo
        F15_mejor_modelo = 0 # Inicializando puntaje F.15, el cual es el que nos vamos a basar para la elección del modelo
        for i in range(len(lista_modelos)):
            modelo = lista_modelos[i]
            modelo.fit(X_train,Y_train)
            Y_pred = modelo.predict(X_test)
            cm = confusion_matrix(Y_test,Y_pred,labels = [0, 1])
            True_posit=cm[0][0]
            True_neg=cm[1][1]
            False_neg=[1][0]
            False_posit=cm[0][1]
            Total = True_posit+True_neg+False_neg+False_posit
            Accuracy = (True_posit+True_neg)/Total
            Accuracy_pass = (True_neg)/(True_neg+False_posit)
            Accuracy_fail = (True_posit)/(True_posit+False_neg)
            F15=((1+1.5*1.5)*True_posit)/((1+1.5*1.5)*True_posit+(1.5*1.5)*False_neg+False_posit)

            if F15 > F15_mejor_modelo:
                F15_mejor_modelo = F15
                mejor_modelo = modelo

            #print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------
def seleccionar_guardar_modelo_general_1(materia,nombre_materia):
    """
    Guarda el mejor modelo sobre una materia específica en disco.
    El analisis es realizado con las notas del corte 1.
    
    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    mejor_modelo1,F15 = mejor_modelo_general_2(materia)
    #Guardar el modelo en disco
    filename = "modelos/mejor_modelo_"+nombre_materia+"1.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
def seleccionar_guardar_modelo_1(materia,nombre_materia):
    """
    Guarda el mejor modelo sobre una materia específica.
    El analisis es realizado con las notas del corte 1.
    
    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    modelo_general_nombre = "Modelo_General"
    filename = "modelos/mejor_modelo_"+modelo_general_nombre+"1.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    mejor_modelo1,F15 = mejor_modelo_1(materia,modelo_general)
    #Guardar el modelo en disco
    filename = "modelos/mejor_modelo_"+nombre_materia+"1.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
def cargar_modelo_1(nombre_materia):
    """
    Carga un modelo de prediccion que usa el corte 1.

    PARAMETROS:
        nombre_materia: string del nombre de la materia para cargar el modelo

    RETORNA:
        loaded_model: mejor modelo asociado a la materia elegida
    """
    filename = "modelos/mejor_modelo_"+nombre_materia+"1.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loadel_model
#--------------------------------------------------------------------------------------------------------------------
def guardar_mejor_modelo_todas_materias_1(df_completo):
    """
    Guarda el mejor modelo para todas las materias analizando el corte 1.

    PARAMETROS:
        df_completo: dataframe con los datos de todos los estudiantes
    """
    materias = pd.DataFrame(df_completo.groupby("Nombre_Asignatura")).reset_index()
    lista_materias = []
    for index,row in materias.iterrows():
        lista_materias.append(row[0])
    for i in range(len(lista_materias)):
        nombre_materia = lista_materias[i]
        materia = df_completo[df_completo["Nombre_Asignatura"] == nombre_materia]
        seleccionar_guardar_modelo_1(materia,nombre_materia)
#--------------------------------------------------------------------------------------------------------------------
def devolucion_estudiantes_riesgos_1(nombre_materia,materia):
    """
    Retorna dataframe de estudiantes que el modelo predijo que van a perder

    PARAMETROS:
        nombre_materia: nombre de la materia que selecciona para cargar el modelo (puede ser el nombre del archivo con el modelo general)
        materia: dataframe con los datos de las notas de la materia especificada

    RETORNA:
        estudiantes: dataframe con los estudiantes que se predijo que van a perder la materia
    """
    # NOTA: Los datos en materia corresponden a la tabla de datos del semestre actual para sacar las alertas
    loaded_model = cargar_modelo_1(nombre_materia)
    X_test = materia[["Nota_1er_Corte"]]
    Y_pred = loaded_model.predict(X_test)
    Prediccion = X_test
    Prediccion["Pred"]=Y_pred
    idx = Prediccion.index[Prediccion["Pred"]==0]
    estudiantes = materia.loc[idx]
    return estudiantes
