#!/usr/bin/env python3

# Standard library imports
from pathlib import Path
import pickle
import os
import shutil

# Third party imports
import pandas as pd
import psycopg2
from sklearn import svm
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


global app
global conn
global cur
global file
global lista_modelos

# Global-level variables
app = None
conn = None
cur = None
file = str(Path("").resolve())
lista_modelos = None


# Connection to Database
conn = psycopg2.connect(
    user="postgres",
    password="Jgrccgv",
    host="localhost",
    port="5432",
    database="Epsilon56",
)

conn.set_session(autocommit=True)
cur = conn.cursor()
# app = Flask(__name__)
# app.secret_key = secrets.token_bytes(nbytes=16)

# NOTA: Variable global para modelos
lista_modelos = [
    GaussianNB(),
    LogisticRegression(),
    DecisionTreeClassifier(),
    KNeighborsClassifier(
        n_neighbors=2),
    svm.SVC(
        kernel='rbf')]
    # IMPORTANTE: puede agregar modelos a esta lista con distintos parametros
    # como prefiera quien maneje esto


# =======================================================================================================================
# FUNCIONES DE MODELOS PARA SOLO EL PRIMER CORTE

def funcion_paso(x):
    """
    Funcion necesaria para crear la columna Paso en el dataframe.

    PARAMETROS:
        x: nota final

    RETORNA:
        1 si el estudiante paso (x >= 3) o 0 si perdio (x < 3)
        como etiqueta para modelos de prediccion
    """
    if(x >= 3):
        return 1
    elif(x < 3):
        return 0
# -----------------------------------------------------------------------------


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
    X = materia[["nota1", "nota2"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    mejor_modelo = lista_modelos[0]  # Inicializando para eleccion de modelo
    # Inicializando puntaje F.15, el cual es el que nos vamos a basar para la
    # elección del modelo
    F15_mejor_modelo = 0
    for i in range(len(lista_modelos)):
        modelo = lista_modelos[i]
        modelo.fit(X_train, Y_train)
        Y_pred = modelo.predict(X_test)
        cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
        True_posit = cm[0][0]
        True_neg = cm[1][1]
        False_neg = [1][0]
        False_posit = cm[0][1]
        Total = True_posit + True_neg + False_neg + False_posit
        Accuracy = (True_posit + True_neg) / Total
        Accuracy_pass = (True_neg) / (True_neg + False_posit)
        Accuracy_fail = (True_posit) / (True_posit + False_neg)
        F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                                True_posit + (1.5 * 1.5) * False_neg + False_posit)

        if F15 > F15_mejor_modelo:
            F15_mejor_modelo = F15
            mejor_modelo = modelo

        print(r"F_{1.5}$:" + str(F15))
    return mejor_modelo, F15_mejor_modelo
# ------------------------------------------------------------------------------


def mejor_modelo_2(materia, modelo_general):
    """
    Determina el mejor modelo para una materia teniendo en cuenta las clases
    en las que todos pasaron.
    El analisis es realizado con las notas de los cortes 1 y 2.

    PARAMETROS:
        materia: dataframe con los datos de una materia especifica
        modelo_genera: modelo general pre-establecido

    RETORNA:
        mejor_modelo: modelo correspondiente al modelo general
        F_15_mejor_modelo: puntaje F15 asociado al modelo general

    """
    indice = -1
    X = materia[["nota1", "nota2"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    if Y_train["Paso"].nunique(
    ) == 1:  # Codigo para saber si solo posee una clase de prediccion o dos
        Y_pred = modelo_general.predict(X_test)
        cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
        True_posit = cm[0][0]
        True_neg = cm[1][1]
        False_neg = [1][0]
        False_posit = cm[0][1]
        Total = True_posit + True_neg + False_neg + False_posit
        Accuracy = (True_posit + True_neg) / Total
        Accuracy_pass = (True_neg) / (True_neg + False_posit)
        Accuracy_fail = (True_posit) / (True_posit + False_neg)
        F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                                True_posit + (1.5 * 1.5) * False_neg + False_posit)
        return modelo_general, F15
    else:
        # Inicializando para eleccion de modelo
        mejor_modelo = lista_modelos[0]
        # Inicializando puntaje F.15, el cual es el que nos vamos a basar para
        # la elección del modelo
        F15_mejor_modelo = 0
        for i in range(len(lista_modelos)):
            modelo = lista_modelos[i]
            modelo.fit(X_train, Y_train)
            Y_pred = modelo.predict(X_test)
            cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
            True_posit = cm[0][0]
            True_neg = cm[1][1]
            False_neg = [1][0]
            False_posit = cm[0][1]
            Total = True_posit + True_neg + False_neg + False_posit
            Accuracy = (True_posit + True_neg) / Total
            Accuracy_pass = (True_neg) / (True_neg + False_posit)
            Accuracy_fail = (True_posit) / (True_posit + False_neg)
            F15 = (((1 + 1.5 * 1.5) * True_posit)
                   / ((1 + 1.5 * 1.5) * True_posit + (1.5 * 1.5) * False_neg + False_posit))

            if F15 > F15_mejor_modelo:
                F15_mejor_modelo = F15
                mejor_modelo = modelo
                indice = i

            # print(r"F_{1.5}$:" +str(F15))
        mejor_seg_modelo, F15_mejor_seg_modelo = mejor_segundo_modelo_2(
            materia, mejor_modelo, indice, modelo_general)
        mejor_modelo, F15_mejor_modelo = enssemble(
            mejor_modelo, mejor_seg_modelo, X_train, Y_train, X_test, Y_test)
        return mejor_modelo, F15_mejor_modelo
# --------------------------------------------------------------------------------------------------------------------


def mejor_segundo_modelo_2(materia, mejor_modelo, indice, modelo_general):
    """
    Función que devuelve el segundo mejor modelo de la materia analizando primer y segundo corte

    PARAMETROS:
        materia: dataframe,lista
        indice: indice mejor modelo
        mejor_modelo: mejor modelo estadistico para la materia
        modelo_general: modelo estadistico general para todas las materias

    RETORNA:
        mejor_modelo: segundo mejor modelo
        F_15_mejor_modelo: puntaje F15 asociado al modelo general
    """
    X = materia[["nota1", "nota2"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    indice = -1
    if Y_train["Paso"].nunique(
    ) == 1:  # Codigo para saber si solo posee una clase de prediccion o dos
        Y_pred = modelo_general.predict(X_test)
        cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
        True_posit = cm[0][0]
        True_neg = cm[1][1]
        False_neg = [1][0]
        False_posit = cm[0][1]
        Total = True_posit + True_neg + False_neg + False_posit
        Accuracy = (True_posit + True_neg) / Total
        Accuracy_pass = (True_neg) / (True_neg + False_posit)
        Accuracy_fail = (True_posit) / (True_posit + False_neg)
        F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                                True_posit + (1.5 * 1.5) * False_neg + False_posit)
        return modelo_general, F15
    else:
        # Inicializando para eleccion de modelo
        mejor_modelo = lista_modelos[0]
        # Inicializando puntaje F.15, el cual es el que nos vamos a basar para
        # la elección del modelo
        F15_mejor_modelo = 0
        for i in range(len(lista_modelos)):
            modelo = lista_modelos[i]
            modelo.fit(X_train, Y_train)
            Y_pred = modelo.predict(X_test)
            cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
            True_posit = cm[0][0]
            True_neg = cm[1][1]
            False_neg = [1][0]
            False_posit = cm[0][1]
            Total = True_posit + True_neg + False_neg + False_posit
            Accuracy = (True_posit + True_neg) / Total
            Accuracy_pass = (True_neg) / (True_neg + False_posit)
            Accuracy_fail = (True_posit) / (True_posit + False_neg)
            F15 = (((1 + 1.5 * 1.5) * True_posit)
                   / ((1 + 1.5 * 1.5) * True_posit + (1.5 * 1.5) * False_neg + False_posit))

            if F15 > F15_mejor_modelo:
                F15_mejor_modelo = F15
                mejor_modelo = modelo

            # print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo, F15_mejor_modelo
# --------------------------------------------------------------------------------------------------------------------


def enssemble(modelo1, modelo2, X_train, Y_train, X_test, Y_test):
    # NOTA: revisar documentacion
    """
    Combina dos modelos de clasificacion usando clasificador de votacion
    (Voting Classifier),funciona tanto para primer corte y segundo corte.

    PARAMETROS:
        modelo1: uno de los modelos que se combina
        modelo2: uno de los modelos que se combina
        X_train: dataframe de entrenamiento
        Y_train: variable independiente de entrenamiento
        X_test: dataframe para testeo de modelo para posterior elección del mejor modelo
        Y_test: variable independiente para hacer test

    RETORNA:
        vot: modelo clasificador de tipo VotingClassifier
        F15: puntaje F15 del VotingClassifier asociado
    """
    estimator = [('1', modelo1), ('2', modelo2)]
    vot = VotingClassifier(estimators=estimator, voting='hard')
    vot.fit(X_train, Y_train)
    Y_pred = vot.predict(X_test)
    cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
    True_posit = cm[0][0]
    True_neg = cm[1][1]
    False_neg = [1][0]
    False_posit = cm[0][1]
    Total = True_posit + True_neg + False_neg + False_posit
    Accuracy = (True_posit + True_neg) / Total
    Accuracy_pass = (True_neg) / (True_neg + False_posit)
    Accuracy_fail = (True_posit) / (True_posit + False_neg)
    F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                            True_posit + (1.5 * 1.5) * False_neg + False_posit)
    return vot, F15
# --------------------------------------------------------------------------------------------------------------------


def seleccionar_guardar_modelo_general_2(materia):
    """
    Guarda el mejor modelo, es decir el modelo general, sobre todas las materias.
    El analisis es realizado con las notas de los cortes 1 y 2.

    PARAMETROS:
        materia: dataframe con las notas de todos las materias de todos los estudiantes
    """
    nombre_materia = "Modelo_General"
    mejor_modelo1, F15 = mejor_modelo_general_2(materia)
    # Guardar el modelo en disco
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1,2.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
# --------------------------------------------------------------------------------------------------------------------


def seleccionar_guardar_modelo_2(materia, nombre_materia):
    """
    Guarda el mejor modelo sobre una materia específica.
    El analisis es realizado con las notas de los cortes 1 y 2.

    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    modelo_general_nombre = "Modelo_General"
    filename = file + "/modelos/mejor_modelo_" + modelo_general_nombre + "1,2.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    mejor_modelo1, F15 = mejor_modelo_2(materia, modelo_general)
    # Guardar el modelo en disco
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1,2.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


def seleccionar_guardar_modelo_2_gen(materia, nombre_materia):
    """
    Esta funcion selecciona el modelo general para esta materia
    en caso de que no se pueda seleccionar un modelo específico para la misma
    El análisis de los modelos para esta funcion es sobre los cortes 1 y 2.

    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    modelo_general_nombre = "Modelo_General"
    filename = file + "/modelos/mejor_modelo_" + modelo_general_nombre + "1,2.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    # Guardar el modelo en disco
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1,2.sav"
    pickle.dump(modelo_general, open(filename, 'wb'))
# --------------------------------------------------------------------------------------------------------------------


def cargar_modelo_2(nombre_materia):
    """
    Carga un modelo de prediccion que usa cortes 1 y 2

    PARAMETROS:
        nombre_materia: string del nombre de la materia para cargar el modelo

    RETORNA:
        loaded_model: mejor modelo asociado a la materia elegida
    """
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1,2.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
# --------------------------------------------------------------------------------------------------------------------


def guardar_mejor_modelo_todas_materias_2(df_completo):
    """
    Guarda el mejor modelo para todas las materias analizando cortes 1 y 2

    PARAMETROS:
        df_completo: dataframe con los datos de todos los estudiantes
    """
    seleccionar_guardar_modelo_general_2(df_completo)
    materias = pd.DataFrame(df_completo.groupby(
        "nombre_asignatura")).reset_index()
    lista_materias = []
    for index, row in materias.iterrows():
        lista_materias.append(row[0])
    for i in range(len(lista_materias)):
        nombre_materia = lista_materias[i]
        print(nombre_materia)
        materia = df_completo[df_completo["nombre_asignatura"]
                              == nombre_materia]
        if(len(materia.index) >= 4):
            seleccionar_guardar_modelo_2(materia, nombre_materia)
        else:
            seleccionar_guardar_modelo_2_gen(materia, nombre_materia)
# --------------------------------------------------------------------------------------------------------------------


def devolucion_estudiantes_riesgos_2(nombre_materia, materia):
    """
    Retorna dataframe de estudiantes que el modelo predijo que van a perder

    PARAMETROS:
        nombre_materia: nombre de la materia que selecciona para cargar el modelo
            (puede ser el nombre del archivo con el modelo general)
        materia: dataframe con los datos de las notas de la materia especificada

    RETORNA:
        estudiantes: dataframe con los estudiantes que se predijo que van a perder la materia
    """
    loaded_model = cargar_modelo_2(nombre_materia)
    X_test = materia[["nota1", "nota2"]]
    Y_pred = loaded_model.predict(X_test)
    Prediccion = X_test
    Prediccion["Pred"] = Y_pred
    idx = Prediccion.index[Prediccion["Pred"] == 0]
    estudiantes = materia.loc[idx]
    return estudiantes
# --------------------------------------------------------------------------------------------------------------------
#
# ====================================================================================================================
# ====================================================================================================================
# ====================================================================================================================
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
    X = materia[["nota1"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    mejor_modelo = lista_modelos[0]  # Inicializando para eleccion de modelo
    # Inicializando puntaje F.15, el cual es el que nos vamos a basar para la
    # elección del modelo
    F15_mejor_modelo = 0
    for i in range(len(lista_modelos)):
        modelo = lista_modelos[i]
        modelo.fit(X_train, Y_train)
        Y_pred = modelo.predict(X_test)
        cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
        True_posit = cm[0][0]
        True_neg = cm[1][1]
        False_neg = [1][0]
        False_posit = cm[0][1]
        Total = True_posit + True_neg + False_neg + False_posit
        Accuracy = (True_posit + True_neg) / Total
        Accuracy_pass = (True_neg) / (True_neg + False_posit)
        Accuracy_fail = (True_posit) / (True_posit + False_neg)
        F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                                True_posit + (1.5 * 1.5) * False_neg + False_posit)

        if F15 > F15_mejor_modelo:
            F15_mejor_modelo = F15
            mejor_modelo = modelo

        print(r"F_{1.5}$:" + str(F15))
    return mejor_modelo, F15_mejor_modelo
# --------------------------------------------------------------------------------------------------------------------


def mejor_modelo_1(materia, modelo_general):
    """
    Determina el mejor modelo para una materia teniendo en cuenta las clases
    en las que todos pasaron.
    El analisis es realizado con las notas del corte 1 y 2.

    PARAMETROS:
        materia: dataframe con los datos de una materia especifica
        modelo_genera: modelo general pre-establecido

    RETORNA:
        mejor_modelo: modelo correspondiente al modelo general
        F_15_mejor_modelo: puntaje F15 asociado al modelo geenral
    """
    indice = -1
    X = materia[["nota1"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    if Y_train["Paso"].nunique(
    ) == 1:  # Codigo para saber si solo posee una clase de prediccion o dos
        Y_pred = modelo_general.predict(X_test)
        cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
        True_posit = cm[0][0]
        True_neg = cm[1][1]
        False_neg = [1][0]
        False_posit = cm[0][1]
        Total = True_posit + True_neg + False_neg + False_posit
        Accuracy = (True_posit + True_neg) / Total
        Accuracy_pass = (True_neg) / (True_neg + False_posit)
        Accuracy_fail = (True_posit) / (True_posit + False_neg)
        F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                                True_posit + (1.5 * 1.5) * False_neg + False_posit)
        return modelo_general, F15
    else:
        # Inicializando para eleccion de modelo
        mejor_modelo = lista_modelos[0]
        # Inicializando puntaje F.15, el cual es el que nos vamos a basar para
        # la elección del modelo
        F15_mejor_modelo = 0
        for i in range(len(lista_modelos)):
            modelo = lista_modelos[i]
            modelo.fit(X_train, Y_train)
            Y_pred = modelo.predict(X_test)
            cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
            True_posit = cm[0][0]
            True_neg = cm[1][1]
            False_neg = [1][0]
            False_posit = cm[0][1]
            Total = True_posit + True_neg + False_neg + False_posit
            Accuracy = (True_posit + True_neg) / Total
            Accuracy_pass = (True_neg) / (True_neg + False_posit)
            Accuracy_fail = (True_posit) / (True_posit + False_neg)
            F15 = (((1 + 1.5 * 1.5) * True_posit)
                   / ((1 + 1.5 * 1.5) * True_posit + (1.5 * 1.5) * False_neg + False_posit))

            if F15 > F15_mejor_modelo:
                F15_mejor_modelo = F15
                mejor_modelo = modelo
                indice = i

        mejor_seg_modelo, F15_mejor_seg_modelo = mejor_segundo_modelo_1(
            materia, mejor_modelo, indice, modelo_general)
        mejor_modelo, F15_mejor_modelo = enssemble(
            mejor_modelo, mejor_seg_modelo, X_train, Y_train, X_test, Y_test)

        # print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo, F15_mejor_modelo
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


def mejor_segundo_modelo_1(materia, mejor_modelo, indice, modelo_general):
    """
    Función que devuelve el segundo mejor modelo de la materia analizando primer corte.

    PARAMETROS:
        materia: dataframe,lista
        indice: indice mejor modelo
        mejor_modelo: mejor modelo estadistico para la materia
        modelo_general: modelo estadistico general para todas las materias

    RETORNA:
        mejor_modelo: segundo mejor modelo
        F_15_mejor_modelo: puntaje F15 asociado al modelo general
    """
    X = materia[["nota1"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    indice = -1
    if Y_train["Paso"].nunique(
    ) == 1:  # Codigo para saber si solo posee una clase de prediccion o dos
        Y_pred = modelo_general.predict(X_test)
        cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
        True_posit = cm[0][0]
        True_neg = cm[1][1]
        False_neg = [1][0]
        False_posit = cm[0][1]
        Total = True_posit + True_neg + False_neg + False_posit
        Accuracy = (True_posit + True_neg) / Total
        Accuracy_pass = (True_neg) / (True_neg + False_posit)
        Accuracy_fail = (True_posit) / (True_posit + False_neg)
        F15 = ((1 + 1.5 * 1.5) * True_posit) / ((1 + 1.5 * 1.5) *
                                                True_posit + (1.5 * 1.5) * False_neg + False_posit)
        return modelo_general, F15
    else:
        # Inicializando para eleccion de modelo
        mejor_modelo = lista_modelos[0]
        # Inicializando puntaje F.15, el cual es el que nos vamos a basar para
        # la elección del modelo
        F15_mejor_modelo = 0
        for i in range(len(lista_modelos)):
            if i != indice:
                modelo = lista_modelos[i]
                modelo.fit(X_train, Y_train)
                Y_pred = modelo.predict(X_test)
                cm = confusion_matrix(Y_test, Y_pred, labels=[0, 1])
                True_posit = cm[0][0]
                True_neg = cm[1][1]
                False_neg = [1][0]
                False_posit = cm[0][1]
                Total = True_posit + True_neg + False_neg + False_posit
                Accuracy = (True_posit + True_neg) / Total
                Accuracy_pass = (True_neg) / (True_neg + False_posit)
                Accuracy_fail = (True_posit) / (True_posit + False_neg)
                F15 = (((1 + 1.5 * 1.5) * True_posit)
                       / ((1 + 1.5 * 1.5) * True_posit + (1.5 * 1.5) * False_neg + False_posit))

                if F15 > F15_mejor_modelo:
                    F15_mejor_modelo = F15
                    mejor_modelo = modelo
                    indice = i

            # print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo, F15_mejor_modelo
# --------------------------------------------------------------------------------------------------------------------


def seleccionar_guardar_modelo_general_1(materia, nombre_materia):
    """
    Guarda el mejor modelo sobre una materia específica en disco.
    El analisis es realizado con las notas del corte 1.

    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    mejor_modelo1, F15 = mejor_modelo_general_1(materia)
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1.sav"
    # print("Modelo General Corte 1 Guardado")
    # print(os.getcwd())
    pickle.dump(mejor_modelo1, open(filename, 'wb'))

# --------------------------------------------------------------------------------------------------------------------


def seleccionar_guardar_modelo_1(materia, nombre_materia):
    """
    Guarda el mejor modelo sobre una materia específica.
    El analisis es realizado con las notas del corte 1.

    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """
    modelo_general_nombre = "Modelo_General"
    filename = file + "/modelos/mejor_modelo_" + modelo_general_nombre + "1.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    mejor_modelo1, F15 = mejor_modelo_1(materia, modelo_general)
    # Guardar el modelo en disco
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
# --------------------------------------------------------------------------------------------------------------------


def seleccionar_guardar_modelo_1_gen(materia, nombre_materia):
    """
    Esta funcion selecciona el modelo general para esta materia
    en caso de que no se pueda seleccionar un modelo específico para la misma
    El análisis de los modelos para esta funcion es sobre el corte 1.

    PARAMETROS:
        materia: dataframe de la materia especificada
        nombre_materia: string para el nombre del archivo del modelo
    """

    modelo_general_nombre = "Modelo_General"
    filename = file + "/modelos/mejor_modelo_" + modelo_general_nombre + "1.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    # Guardar el modelo en disco
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1.sav"
    pickle.dump(modelo_general, open(filename, 'wb'))
# --------------------------------------------------------------------------------------------------------------------


def cargar_modelo_1(nombre_materia):
    """
    Carga un modelo de prediccion que usa el corte 1.

    PARAMETROS:
        nombre_materia: string del nombre de la materia para cargar el modelo

    RETORNA:
        loaded_model: mejor modelo asociado a la materia elegida
    """
    filename = file + "/modelos/mejor_modelo_" + nombre_materia + "1.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
# --------------------------------------------------------------------------------------------------------------------


def guardar_mejor_modelo_todas_materias_1(df_completo):
    """
    Guarda el mejor modelo para todas las materias analizando el corte 1.

    PARAMETROS:
        df_completo: dataframe con los datos de todos los estudiantes
    """
    seleccionar_guardar_modelo_general_1(df_completo, "Modelo_General")
    materias = pd.DataFrame(df_completo.groupby(
        "nombre_asignatura")).reset_index()
    lista_materias = []
    for index, row in materias.iterrows():
        lista_materias.append(row[0])
    for i in range(len(lista_materias)):
        nombre_materia = lista_materias[i]
        materia = df_completo[df_completo["nombre_asignatura"]
                              == nombre_materia]
        if(len(materia.index) >= 4):
            seleccionar_guardar_modelo_1(materia, nombre_materia)
        else:
            seleccionar_guardar_modelo_1_gen(materia, nombre_materia)
# --------------------------------------------------------------------------------------------------------------------


def devolucion_estudiantes_riesgos_1(nombre_materia, materia):
    """
    Retorna dataframe de estudiantes que el modelo predijo que van a perder

    PARAMETROS:
        nombre_materia: nombre de la materia que selecciona para cargar el modelo (puede ser el nombre del archivo con el modelo general)
        materia: dataframe con los datos de las notas de la materia especificada

    RETORNA:
        estudiantes: dataframe con los estudiantes que se predijo que van a perder la materia
    """
    # NOTA: Los datos en materia corresponden a la tabla de datos del semestre
    # actual para sacar las alertas
    loaded_model = cargar_modelo_1(nombre_materia)
    X_test = materia[["nota1"]]
    Y_pred = loaded_model.predict(X_test)
    Prediccion = X_test
    Prediccion["Pred"] = Y_pred
    idx = Prediccion.index[Prediccion["Pred"] == 0]
    estudiantes = materia.loc[idx]
    return estudiantes
# ---------------------------------------------------------------------------------------------------------------
# Funcion de mover modelos de semestre actual a semestre anterior


def mover_modelos(source, destination):
    """
    Mueve todos los archivos de la carpeta fuente a la carpeta destino.
    Si las direcciones son relativas, las direcciones empiezan desde la carpeta
    donde se encuentra el archivo con esta funcion.

    PARAMETROS:
        source: direccion de la carpeta fuente
        destination: direccion de la carpeta destino
    """
    files = os.listdir(source)
    for file in files:
        shutil.move(f"{source}/{file}", destination)

# ------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# Funcion Main
# --------------------------------------------------------------------------------------------------------------------


def model_selection_from_historic_data():
    """
    Funcion de entrenamiento con csv de historico.
    """
    # Esta función fue ejecutada antes de entrgar la aplicación, para obtener los archivos
    # que se encuentran en la carpeta de modelos
    # ---------------------- #
    filename = ("modelos/Información_antes_de_aplicación/"
                "datos_notas_macc_cortes_historico_20172_20201.csv")
    notas = pd.read_csv(filename, encoding='utf-8', header=0, sep=";")
    # Eliminar Nans
    notas = notas.dropna()
    # notas
    # Agregando nota final para predicción:
    notas["Nota_Final"] = notas.apply(
        lambda row: (
            row["Nota 1er Corte"] +
            row["Nota 2do Corte"] +
            row["Nota 3er Corte"] +
            row["Nota 4to Corte"] +
            row["Nota 5to Corte"]) /
        5,
        axis=1)
    notas["Paso"] = notas.apply(
        lambda row: funcion_paso(
            row["Nota_Final"]), axis=1)
    notas = notas.rename(
        columns={
            'Nombre Asignatura': 'nombre_asignatura',
            'Nota 1er Corte': 'nota1',
            'Nota 2do Corte': 'nota2'})
    guardar_mejor_modelo_todas_materias_2(notas)
    guardar_mejor_modelo_todas_materias_1(notas)

# ---------------------------------------------------------------------------------------------------------------------


def model_training():
    """
    Funcion que se encarga de entrenar los modelos.
    """
    # ---------------------- #
    df = pd.read_sql(
        "select est_usr,nombre_asignatura,periodo,anio,nota1,nota2,"
        "round((nota1*porcentaje1+nota2*porcentaje2+nota3*porcentaje3+nota4*"
        "porcentaje4+nota5*porcentaje5)/100,2) as nota_final from resumen",
        conn)
    df["Paso"] = df.apply(lambda row: funcion_paso(row["nota_final"]), axis=1)
    guardar_mejor_modelo_todas_materias_2(df)
    guardar_mejor_modelo_todas_materias_1(df)
# ---------------------------------------------------------------------------------------------------------------------


def prediction_from_trained_models():
    """
    Funcion que se encarga de hacer la predicción de los estudiantes.

    RETORNA:
        lista_estudiantes_alerta: dataframe con los estudiantes con riesgo de perder la materia
    """
    # lista_estudiantes: dataframe
    columnas = ["est_usr", "nombre_asignatura", "nota1", "nota2"]
    lista_estudiantes_alerta = pd.DataFrame(columns=columnas)
    # query obtencion de notas normal
    query1 = """select est_usr,nombre_asignatura,nota1,nota2
                from resumen where periodo = (select max(periodo) from resumen
                where anio =(select max(anio) from resumen ))
                and anio = (select max(anio) from resumen)"""
    # query sin columna segundo corte
    df = pd.read_sql(query1, conn)
    lista_materias = []
    materias = pd.DataFrame(df.groupby("nombre_asignatura")).reset_index()
    for index, row in materias.iterrows():
        lista_materias.append(row[0])

    if df["nota2"].count() == len(
            df.index) & df["nota1"].count() == len(
            df.index):
        print("Entro Prediccion 2 Corte")
        for i in range(len(lista_materias)):
            nombre_materia = lista_materias[i]
            materia = df[df["nombre_asignatura"] == nombre_materia]
            estudiantes = devolucion_estudiantes_riesgos_2(
                nombre_materia, materia)
            lista_estudiantes_alerta = lista_estudiantes_alerta.append(
                estudiantes)

    elif df["nota1"].count() == len(df.index):
        print("Entro Prediccion 1 Corte")
        for i in range(len(lista_materias)):
            nombre_materia = lista_materias[i]
            materia = df[df["nombre_asignatura"] == nombre_materia]
            estudiantes = devolucion_estudiantes_riesgos_1(
                nombre_materia, materia)
            lista_estudiantes_alerta = lista_estudiantes_alerta.append(
                estudiantes)

    return lista_estudiantes_alerta


if __name__ == "__main__":
    pass
    # model_selection_from_historic_data()
    # main1()
    # lista_estudiantes_alerta = main2()
    # print(lista_estudiantes_alerta.head())
