CREATE TABLE Public.mytable(
   Documento_Ingreso     INTEGER  NOT NULL
  ,Documento_Actual      INTEGER  NOT NULL
  ,Codigo                INTEGER  NOT NULL
  ,Apellido_1_Estudiante VARCHAR(100) NOT NULL
  ,Apellido_2_Estudiante VARCHAR(100) NOT NULL
  ,Nombres_Estudiante    VARCHAR(100) NOT NULL
  ,Acceso                VARCHAR(100) NOT NULL
  ,Subacceso             VARCHAR(100) NOT NULL
  ,Correo_Institucional  VARCHAR(100) NOT NULL
  ,Sexo                  VARCHAR(100) NOT NULL
  ,Facultad_o_Escuela    VARCHAR(100) NOT NULL
  ,Programa              VARCHAR(100) NOT NULL
  ,Semestre              INTEGER  NOT NULL
  ,Creditos_inscritos    INTEGER  NOT NULL
  ,Codigo_Asignatura     INTEGER  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      BIT  NOT NULL
  ,Tipologia_Asignatura  VARCHAR(100) NOT NULL
  ,Nota_1er_Corte        NUMERIC(3,1) NOT NULL
  ,Corte_1p              INTEGER  NOT NULL
  ,Nota_2do_Corte        NUMERIC(3,1) NOT NULL
  ,Corte_2p              INTEGER  NOT NULL
  ,Nota_3er_Corte        NUMERIC(3,1) NOT NULL
  ,Corte_3p              INTEGER  NOT NULL
  ,Nota_4to_Corte        NUMERIC(3,1) NOT NULL
  ,Corte_4p              INTEGER  NOT NULL
  ,Nota_5to_Corte        NUMERIC(3,1) NOT NULL
  ,Corte_5p              INTEGER  NOT NULL
	, PRIMARY KEY(Documento_actual,Nombre_Asignatura)
);

COPY Public.mytable FROM 'C:\Users\Miguel Gutierrez\Documents\capstone2020\datos_prueba\Datos_prueba.csv' DELIMITER ',' CSV HEADER ;

Create table Programa(
	 codigo Integer NOT NULL
	,programa VARCHAR(100) NOT NULL
	,facultad_o_escuela VARCHAR(100) NOT NULL
	, PRIMARY KEY(codigo)
);

Create table Estudiante(
	 codigo Integer NOT NULL
	,documento_ingreso Integer NOT NULL
	,acceso VARCHAR(100) NOT NULL
	,subacceso VARCHAR(100) NOT NULL
	,PRIMARY KEY(codigo)
);

Create table Personas(
	 codigo Integer NOT NULL
	,nombres_estudiante VARCHAR(100) NOT NULL
	,apellido_1_estudiante VARCHAR(100) NOT NULL
	,apellido_2_estudiante VARCHAR(100) NOT NULL
	,correo_institucional VARCHAR(100) NOT NULL
	,sexo VARCHAR(100) NOT NULL
	,documento_actual VARCHAR(100) NOT NULL
	,PRIMARY KEY(codigo)
);

Create table Asignaturas(
	 codigo_asignatura VARCHAR(100) NOT NULL
	,nombre_asignatura VARCHAR(100) NOT NULL
	,creditos_asignatura VARCHAR(100) NOT NULL
	,tipologia_asignatura VARCHAR(100) NOT NULL
	,PRIMARY KEY(codigo_asignatura)
)


drop table Asignaturas

select*from mytable

/* Metiendo a la tabla de Programa */
insert into Programa(codigo,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela from mytable

select*from Programa

/* Metiendo a la tabla de Estudiante */

insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso from mytable

select*from Estudiante

/* Metiendo a la tabla de Personas */

insert into Personas(codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual from mytable

select*from Personas

/* Metiendo a la tabla de Asignaturas*/

insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura from mytable

select*from Asignaturas

/* Metiendo a la tabla de Semestre*/

drop table mytable
