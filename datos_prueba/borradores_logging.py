

# Usuario hace log in en la aplicacion

logging(USUARIO,1,'INICIO')

# Usuario hace log out de la aplicacion

logging(USUARIO,1,'SALIR')

# Consulta estudiante de notas y asignaturas

logging(USUARIO,1,'CONSULTA',sobre_que='NOTAS',cuando=PERIODO_ANIO,)

# Consulta profesores periodos

logging(USUARIO,1,'CONSULTA',sobre_que="PERIODOS")

# Consulta profesores asignaturas en un periodo

logging(USUARIO,1,'CONSULTA',sobre_que="ASIGNATURAS",cuando=PERIODO_ANIO)

# Consulta profesores asignatura en particular

logging(USUARIO,1,'CONSULTA',sobre_que="ASIGNATURAS",sobre_quien=ASIGNATURA,grupo=GRUPO,cuando=PERIODO)

# Consulta de administrador sobre estudiantes

logging(USUARIO,1,'CONSULTA',sobre_que="ESTUDIANTES",cuando=PERIODO_ANIO)

# Consulta de administrador sobre un estudiante

logging(USUARIO,1,'CONSULTA',sobre_que="ESTUDIANTES",sobre_quien=USUARIO_ESTUDIANTE,cuando=PERIODO_ANIO)

# Consulta de administrador sobre profesores

logging(USUARIO,1,'CONSULTA',sobre_que="PROFESORES")

# Consulta de administrador sobre un profesor

logging(USUARIO,1,'CONSULTA',sobre_que="PROFESORES",sobre_quien=USUARIO_PROFESOR)

# Consulta de administrador sobre un profesor en un periodo

logging(USUARIO,1,'CONSULTA',sobre_que="PROFESORES",sobre_quien=USUARIO_PROFESOR,cuando=PERIODO_ANIO)

# Consulta de administrador sobre un profesor en un periodo y una asignatura

logging(USUARIO,1,'CONSULTA',sobre_que="PROFESORES",sobre_quien=URUSARIO_PROFESOR,asignatura=ASIGNATURA,grupo=GRUPO,cuando=PERIODO_ANIO)

# Consulta administrador asignaturas

logging(USUARIO,1,'CONSULTA',sobre_que="ASIGNATURAS")

# Consulta administrador asignaturas en un periodo

logging(USUARIO,1,'CONSULTA',sobre_que="ASIGNATURAS",cuando=PERIODO_ANIO)

# Consulta administrador asignaturas en un periodo, materia en particular

logging(USUARIO,1,'CONSULTA',sobre_que="ASIGNATURAS",asignatura=ASIGANTURA,grupo=GRUPO,cuando=PERIODO_ANIO)

# Edicion de notas

logging(USUARIO,2,'EDICION',sobre_que="NOTAS",sobre_quien=USUARIO_ESTUDIANTE,asignatura=ASIGANTURA,grupo=GRUPO,cuando=PERIODO_ANIO,notas_antes=NOTAS_ANTES,notas_despues=NOTAS_DESPUES)

# Edicion de porcentaje

logging(USUARIO,2,'EDICION',sobre_que="PORCENTAJE",asignatura=ASIGANTURA,grupo=GRUPO,cuando=PERIODO_ANIO,notas_antes=PORCENTAJE_ANTES,notas_despues=PORCENTAJE_DESPUES)

# Edicion de contrasdena

logging(USAURIO,2,'EDICION',sobre_que='CONTRASENA')

# Exportar notas estudiante

loggin(user_name,1,'EXPORTAR',sobre_que='NOTAS',sobre_quien=USER_ESTUDIANTE,cuando=PERIODO)

# Exportar notas de asignatura

loggin(user_name,1,'EXPORTAR',sobre_que='NOTAS',asignatura=ASIGNATURA,grupo=GRUPO,cuando=PERIODO)

# Exportar reporte de estudiante en una asignautra
loggin(USER_NAME,1,'EXPORTAR',sobre_que='REPORTE',sobre_quien=USER_ESTUDIANTE,asignatura=ASIGNATURA,grupo=GRUPO,cuando=PERIODO)

# Exportar reporte de asignatura
loggin(USER_NAME,1,'EXPORTAR',sobre_que='REPORTE',asignatura=ASIGNATURA,grupo=GRUPO,cuando=PERIODO)


# Insertar informacion de estudiantes

loggin(USER_NAME,3,'IMPORTAR',sobre_que='DATOS',sobre_que='ESTUDIANTES',cuando=PERIODO)

# Insertar informacion de profesores 

loggin(USER_NAME,3,'IMPORTAR',sobre_que='DATOS',sobre_quien='PROFESORES',cuando=PERIODO)

# Insertar informacion de materias

loggin(USER_NAME,3,'IMPORTAR',sobre_que='DATOS',sobre_quien='MATERIAS',asignatura=ASIGNATURA,grupo=GRUPO,cuando=PERIODO)
