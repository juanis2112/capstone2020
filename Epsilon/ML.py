import psycopg2
import pandas as pd
import sqlalchemy
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
from sklearn.ensemble import VotingClassifier
import pickle
import os
from pathlib import Path

# Connection to DataBase
conn = psycopg2.connect(user="postgres",
                        password="1234",
                        host="localhost",
                        port="5432",
                        database="capstone20201",)

conn.set_session(autocommit=True)
cur = conn.cursor()
#app = Flask(__name__)
#app.secret_key = 'mysecretkey'
#-------------------------------------------------------------------------
# Obtener path relativo al script
file = os.path.dirname(__file__)
# NOTA: Variable global para modelos. El que quiera debe crear la lista con todos los modelos afuera de la funcion?
lista_modelos =[GaussianNB(),LogisticRegression(),DecisionTreeClassifier(),KNeighborsClassifier(n_neighbors=2),svm.SVC(kernel='rbf')]
#=======================================================================================================================
# FUNCIONES DE MODELOS PARA SOLO EL PRIMER CORTE

# Funcion necesaria para crear la columna Paso en el dataframe
def funcion_paso(x):
    #x: nota final
    #return si paso o perdio como etiquetas para modelos de predicción
    if(x >= 3):
        return 1
    elif(x <3):
        return 0
#-----------------------------------------------------------------------------
# Funcion que determina el mejor modelo (modelo general sobre todas las materias) sobre todos los datos a partir de las notas de los 2 primeros cortes
def mejor_modelo_general_2(materia):
    # materia: dataframe con notas en todas las materias
    X = materia[["nota1","nota2"]]
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
# Funcion que determina el mejor modelo para una materia teniendo en cuenta las clases en las que todos pasaron
def mejor_modelo_2(materia,modelo_general):
    # materia: dataframe con los datos de una materia especifica
    # modelo_genera: modelo general pre-establecido
    indice = -1
    X = materia[["nota1","nota2"]]
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
                indice = i

            #print(r"F_{1.5}$:" +str(F15))
        mejor_seg_modelo,F15_mejor_seg_modelo=mejor_segundo_modelo_2(materia,mejor_modelo,indice,modelo_general)
        mejor_modelo,F15_mejor_modelo = enssemble(mejor_modelo,mejor_seg_modelo,X_train,Y_train,X_test,Y_test)
        return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------
# Función que devuelve el segundo mejor modelo de la materia de primer y segundo corte
def mejor_segundo_modelo_2(materia,mejor_modelo,indice,modelo_general):
    #materia : dataframe,lista
    #mejor_modelo : modelo
    #indice : indice mejor modelo
    #return: segundo mejor modelo,puntaje F_15,y su respectivo indice
    X = materia[["nota1","nota2"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    indice = -1
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
                indice = i

            #print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------
# Funciona que combina dos modelos de clasificacion,funciona tanto para primer corte y segundo corte
def enssemble(modelo1,modelo2,X_train,Y_train,X_test,Y_test):
    #modelo 1
    #modelo 2
    #X_train: dataframde de entrenamiento
    #Y_train : variable independeinte de entrenamiento
    #X_test,Y_test: dataframe para testeo de modelo para posterior elección del mejor modelo
    estimator = [('1',modelo1),('2',modelo2)]
    vot= VotingClassifier(estimators = estimator, voting = 'hard')
    vot.fit(X_train, Y_train)
    Y_pred = vot.predict(X_test)
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
    return vot,F15
#--------------------------------------------------------------------------------------------------------------------
# Funcion para guardar el mejor modelo, es decir el modelo general, sobre todas las materias
def seleccionar_guardar_modelo_general_2(materia):
    # materia: dataframe con las notas de todos las materias de todos los estudiantes
    nombre_materia = "Modelo_General"
    mejor_modelo1,F15 = mejor_modelo_general_2(materia)
    #Guardar el modelo en disco
    filename = file+"/modelos/mejor_modelo_"+nombre_materia+"1,2.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
# Funcion para guardar el mejor modelo sobre una materia específica
def seleccionar_guardar_modelo_2(materia,nombre_materia):
    # materia: dataframe de la materia especificada
    # nombre_materia: string para el nombre del archivo del modelo
    modelo_general_nombre = "Modelo_General"
    filename = file+"/modelos/mejor_modelo_"+modelo_general_nombre+"1,2.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    mejor_modelo1,F15 = mejor_modelo_2(materia,modelo_general)
    #Guardar el modelo en disco
    filename = file+"/modelos/mejor_modelo_"+nombre_materia+"1,2.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
# Funcion que carga un modelo que usa cortes 1 y 2
def cargar_modelo_2(nombre_materia):
    filename = file+"/modelos/mejor_modelo_"+nombre_materia+"1,2.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
#--------------------------------------------------------------------------------------------------------------------
# Funcion que guarda el mejor modelo para todas las materias analizando cortes 1 y 2
def guardar_mejor_modelo_todas_materias_2(df_completo):
    # df_completo: dataframe con los datos de todos los estudiantes
    seleccionar_guardar_modelo_general_2(df_completo)
    materias = pd.DataFrame(df_completo.groupby("nombre_asignatura")).reset_index()
    lista_materias = []
    for index,row in materias.iterrows():
        lista_materias.append(row[0])
    for i in range(len(lista_materias)):
        nombre_materia = lista_materias[i]
        materia = df_completo[df_completo["nombre_asignatura"] == nombre_materia]
        seleccionar_guardar_modelo_2(materia,nombre_materia)
#--------------------------------------------------------------------------------------------------------------------
# Funcion que retorna dataframe de estudiantes que el modelo predijo que van a perder
def devolucion_estudiantes_riesgos_2(nombre_materia,materia):
    # nombre_materia: nombre de la materia que selecciona para cargar el modelo (puede ser el nombre del archivo con el modelo general)
    # materia: dataframe con los datos de las notas de la materia especificada
    # NOTA: Los datos en materia corresponden a la tabla de datos del semestre actual para sacar las alertas
    loaded_model = cargar_modelo_2(nombre_materia)
    X_test = materia[["nota1","nota2"]]
    Y_pred = loaded_model.predict(X_test)
    Prediccion = X_test
    Prediccion["Pred"]=Y_pred
    idx = Prediccion.index[Prediccion["Pred"]==0]
    estudiantes = materia.loc[idx]
    return estudiantes
#--------------------------------------------------------------------------------------------------------------------
#
#====================================================================================================================
#====================================================================================================================
#====================================================================================================================
# FUNCIONES DE MODELOS PARA SOLO EL PRIMER CORTE
def mejor_modelo_general_1(materia):
    # materia: dataframe con notas en todas las materias
    X = materia[["nota1"]]
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
# Funcion que determina el mejor modelo para una materia teniendo en cuenta las clases en las que todos pasaron
def mejor_modelo_1(materia,modelo_general):
    # materia: dataframe con los datos de una materia especifica
    # modelo_genera: modelo general pre-establecido
    indice = -1
    X = materia[["nota1"]]
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
                indice = i

        mejor_seg_modelo,F15_mejor_seg_modelo=mejor_segundo_modelo_1(materia,mejor_modelo,indice,modelo_general)
        mejor_modelo,F15_mejor_modelo = enssemble(mejor_modelo,mejor_seg_modelo,X_train,Y_train,X_test,Y_test)

            #print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# Función que devuelve el segundo mejor modelo de la materia de primer y segundo corte
def mejor_segundo_modelo_1(materia,mejor_modelo,indice,modelo_general):
    #materia : dataframe,lista
    #mejor_modelo : modelo
    #indice : indice mejor modelo
    #return: segundo mejor modelo,puntaje F_15,y su respectivo indice
    X = materia[["nota1"]]
    Y = materia[["Paso"]]
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)
    indice = -1
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
            if i != indice:
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
                    indice = i

            #print(r"F_{1.5}$:" +str(F15))
        return mejor_modelo,F15_mejor_modelo
#--------------------------------------------------------------------------------------------------------------------
# Funcion para guardar el mejor modelo, es decir el modelo general, sobre todas las materias
def seleccionar_guardar_modelo_general_1(materia,nombre_materia):
    # materia: dataframe con las notas de todos las materias de todos los estudiantes
    #Guardar el modelo en disco
    mejor_modelo1,F15 = mejor_modelo_general_1(materia)
    filename = file+"/modelos/mejor_modelo_"+nombre_materia+"1.sav"
    print("Modelo General Corte 1 Guardado")
    print(os.getcwd())
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
    
#--------------------------------------------------------------------------------------------------------------------
def seleccionar_guardar_modelo_1(materia,nombre_materia):
    # materia: dataframe de la materia especificada
    # nombre_materia: string para el nombre del archivo del modelo
    modelo_general_nombre = "Modelo_General"
    filename = file+"/modelos/mejor_modelo_"+modelo_general_nombre+"1.sav"
    modelo_general = pickle.load(open(filename, 'rb'))
    mejor_modelo1,F15 = mejor_modelo_1(materia,modelo_general)
    #Guardar el modelo en disco
    filename = file+"/modelos/mejor_modelo_"+nombre_materia+"1.sav"
    pickle.dump(mejor_modelo1, open(filename, 'wb'))
#--------------------------------------------------------------------------------------------------------------------
# Funcion que carga un modelo que usa corte 1
def cargar_modelo_1(nombre_materia):
    filename = file+"/modelos/mejor_modelo_"+nombre_materia+"1.sav"
    loaded_model = pickle.load(open(filename, 'rb'))
    return loaded_model
#--------------------------------------------------------------------------------------------------------------------
# Funcion que guarda el mejor modelo para todas las materias analizando corte 1
# NOTA: Probar funcion
def guardar_mejor_modelo_todas_materias_1(df_completo):
    # df_completo: dataframe con los datos de todos los estudiantes
    seleccionar_guardar_modelo_general_1(df_completo,"Modelo_General")
    materias = pd.DataFrame(df_completo.groupby("nombre_asignatura")).reset_index()
    lista_materias = []
    for index,row in materias.iterrows():
        lista_materias.append(row[0])
    for i in range(len(lista_materias)):
        nombre_materia = lista_materias[i]
        materia = df_completo[df_completo["nombre_asignatura"] == nombre_materia]
        seleccionar_guardar_modelo_1(materia,nombre_materia)
#--------------------------------------------------------------------------------------------------------------------
# Funcion que retorna dataframe de estudiantes que el modelo predijo que van a perder
def devolucion_estudiantes_riesgos_1(nombre_materia,materia):
    # nombre_materia: nombre de la materia que selecciona para cargar el modelo (puede ser el nombre del archivo con el modelo general)
    # materia: dataframe con los datos de las notas de la materia especificada
    # NOTA: Los datos en materia corresponden a la tabla de datos del semestre actual para sacar las alertas
    loaded_model = cargar_modelo_1(nombre_materia)
    X_test = materia[["nota1"]]
    Y_pred = loaded_model.predict(X_test)
    Prediccion = X_test
    Prediccion["Pred"]=Y_pred
    idx = Prediccion.index[Prediccion["Pred"]==0]
    estudiantes = materia.loc[idx]
    return estudiantes
#-------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# Funcion Main
#--------------------------------------------------------------------------------------------------------------------
def main1():
    #----------------------#
    df =  pd.read_sql("""select est_usr,nombre_asignatura,periodo,anio,nota1,nota2,round((nota1*porcentaje1+nota2*porcentaje2+nota3*porcentaje3+nota4*porcentaje4+nota5*porcentaje5)/100,2) as nota_final from resumen""",conn)
    df["Paso"] = df.apply(lambda row: funcion_paso(row["nota_final"]),axis=1 )
    lista_modelos =[GaussianNB(),LogisticRegression(),DecisionTreeClassifier(),KNeighborsClassifier(),svm.SVC(kernel='rbf')]
    if df["nota2"].count()==len(df.index) & df["nota_final"].count()==len(df.index):
        guardar_mejor_modelo_todas_materias_2(df)
    elif df["nota1"].count()==len(df.index) & df["nota_final"].count()==len(df.index):
        guardar_mejor_modelo_todas_materias_1(df)

def main2():
    #lista_estudiantes: dataframe
    columnas = ["est_usr","nombre_asignatura","nota1","nota2"]
    lista_estudiantes_alerta =pd.DataFrame(columns = columnas)
    #query obtencion de notas normal
    query2="""select est_usr,nombre_asignatura,nota1,nota2
    from resumen where periodo = (select max(periodo) from resumen where anio =(select max(anio) from resumen )) and anio = (select max(anio) from resumen)"""
    #query sin columna segundo corte
    query1 = """update toma  set nota2 = NULL where anio = (select max(anio) from resumen) and periodo = (select max(periodo) from resumen where anio = (select max(anio) from resumen))"""
    df =  pd.read_sql(query2,conn)
    print(df.head())
    print(lista_estudiantes_alerta.head())
    lista_materias = []
    materias = pd.DataFrame(df.groupby("nombre_asignatura")).reset_index()
    for index,row in materias.iterrows():
        lista_materias.append(row[0])

    if df["nota2"].count()==len(df.index) & df["nota1"].count()==len(df.index):
        print("Entro Prediccion 2 Corte")
        for i in range(len(lista_materias)):
            nombre_materia = lista_materias[i]
            materia = df[df["nombre_asignatura"] == nombre_materia]
            estudiantes = devolucion_estudiantes_riesgos_2(nombre_materia,materia)
            lista_estudiantes_alerta=lista_estudiantes_alerta.append(estudiantes)

    elif df["nota1"].count()==len(df.index):
        print("Entro Prediccion 1 Corte")
        for i in range(len(lista_materias)):
            nombre_materia = lista_materias[i]
            materia = df[df["nombre_asignatura"] == nombre_materia]
            estudiantes = devolucion_estudiantes_riesgos_1(nombre_materia,materia)
            lista_estudiantes_alerta=lista_estudiantes_alerta.append(estudiantes)


    return lista_estudiantes_alerta

#main1()
lista_estudiantes_alerta = main2()
print(lista_estudiantes_alerta.head())