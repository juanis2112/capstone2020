# ALERTA PARA ESTUDIANTES
# 1. Alerta Nivel nota baja: la nota del estudiante en el corte se encuentra entre [2,3)
# 2. Alerta Nivel nota muy baja: la nota del estudiante en el corte se encuentra entre [0,2)

def alerta_estudiante_materia(materia,corte):
    # Funcion que recibe el dataframe de una materia con sus estudiantes y notas respectivas y saca alertas en un corte determinado
    # materia: data frame de una materia especifica
    # corte: nombre del corte sobre el cual se saca alertas
        for index,row in materia.iterrows(): #Por cada row(estudiante) vamos viendo si el estudiante en ese corte saco alguna nota baja
            if row[corte] < 3 and row[corte] >= 2: #row[corte] es la nota de la materia del estudiante ne esa asignatura
                print("El Estudiante "+ row["Nombres_Estudiante"]+  " se encuentra en Alerta nota baja, en " + corte +" en la materia " + row["Nombre_Asignatura"])
            elif row[corte] < 2:
                print("El Estudiante "+ row["Nombres_Estudiante"]+  " se encuentra en Alerta nota muy baja en "+ corte+" en la materia " + row["Nombre_Asignatura"])
#--------------------------------------------------------------------------------
def alerta_corte(corte,df):
    # Funcion saca las alertas para un corte para todas las materias
    # corte: string con el nombre del corte
    # df: dataframe con las materias que ven todos los estudiantes y sus notas (df_completo)
    for i in asignaturas:
        materia = df[df["Nombre_Asignatura"]== i] #obtiene la tabla de la asginatura en es especifico
        alerta_estudiante_materia(materia,corte)
#--------------------------------------------------------------------------------
def cortes_acumulados(inicial,final,df):
    # Funcion que saca alertas por cortes acumulados para todos los estudiantes
    # inicial: corte inicial para el promedio acumulado (numero)
    # final: corte final para el promedio acumulado (numero)
    # df: dataframe con las materias que ven todos los estudiantes y sus notas (df_completo)
    acumulado =[]
    for j in asignaturas:
        # primero se recorre todas las asignaturas
            materia = df[df["Nombre_Asignatura"]== j]
            for index,row in materia.iterrows():
                num = 0
                den = 0
                for i in range(inicial-1,final):
                    # Luego recorremos los cortes especificados
                    num = num + row[cortes[i]]*row[porcentajes[i]]
                    den = den + row[porcentajes[i]]
                    prom_acum = num/den
                if prom_acum >= 2 and prom_acum < 3:
                        print("El Estudiante "+ row["Nombres_Estudiante"]+
                          " se encuentra en Alerta nota baja, en el corte acumulado ("+str(inicial)+","+str(final)+") en la materia " + j )
                elif prom_acum < 2:
                        print("El Estudiante "+ row["Nombres_Estudiante"]+
                              " se encuentra en Alerta nota MUY baja, en el corte acumulado ("+str(inicial)+","+str(final) +") en la materia " + j )
#--------------------------------------------------------------------------------
#--------------------------------------------------------------------------------
# ALERTA POR MATERIAS
def alerta_materia_corte(nombre_materia,num_corte,df):
    # Funcion  que levanta alerta para materias por corte
    # nombre_materia: nombre de la asigntura
    # num_corte: numero del corte del semestre (entero de 1 a 5)
    # df: dataframe sobre el cual se hace el análisis
    asignatura = df[df["Nombre_Asignatura"]==nombre_materia]
    prom_corte = asignatura[cortes[num_corte-1]].mean()
    if prom_corte >= 2 and prom_corte < 3:
        print("El promedio de "+nombre_materia+" en el corte "+str(num_corte)+" es BAJO")
    elif prom_corte < 2:
        print("El promedio de "+nombre_materia+" en el corte"+str(num_corte)+" es MUY BAJO")
#--------------------------------------------------------------------------------
def alerta_materias_acumulado(nombre_materia,inicial,final,df):
    # Funcion que levanta alerta para materias por promedio acumulado
    # nombre_materia: nombre de la asignatura
    # inicial: numero del corte inicial sobre el cual se calcula el promedio acumulado
    # final: numero del corte final sobre el cual se calcula el promedio acumulado
    # df: dataframe dobre el cual se hace el analisis
    num = 0
    den = 0
    asignatura = df[df["Nombre_Asignatura"]==nombre_materia]
    for i in range(inicial-1,final):
        # NOTA: Sacar el peso de manera mas optima
        peso = asignatura[porcentajes[i]].mean()
        num = num + asignatura[cortes[i]].mean()*peso
        den = den + peso
    prom_acum_mat = num/den
    if prom_acum_mat >= 2 and prom_acum_mat < 3:
        print("El promedio acumulado de "+str(inicial)+","+str(final)+" "+nombre_materia+" es BAJO")
    elif prom_acum_mat < 2:
        print("El promedio acumulado de "+str(inicial)+","+str(final)+" "+nombre_materia+" es MUY BAJO")
#--------------------------------------------------------------------------------
def materia_alert(df,corte):
    # Funcion que saca las materias en un corte sobre todas las asignaturas
    # df: dataframe con todas los estudiantes, materias que ven y sus notas
    # corte: numero del corte del semestre (entero de 1 a 5)
    for i in asignaturas:
        alerta_materia_corte(i,corte,df)
#--------------------------------------------------------------------------------
def materia_alert_acumulado(df,inicial,final):
    # Funcion levanta alerta para todos los cursos dictados por cortes acumulados
    # df: dataframe dobre el cual se hace el analisis
    # inicial: numero del corte inicial sobre el cual se calcula el promedio acumulado
    # final: numero del corte final sobre el cual se calcula el promedio acumulado
    for i in asignaturas: #recorre todas las materias en busca de materias a las que todos los estudiantes les haya ido mal
        alerta_materias_acumulado(i,inicial,final,df)