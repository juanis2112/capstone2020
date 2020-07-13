-- INSERCION 2018_1
CREATE TABLE Public.tablaEstudiante(
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
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

COPY Public.tablaEstudiante FROM '/home/felipe/Escritorio/F.G.S/CAPSTON/capstone2020/datos_prueba/Datos_2018_1.csv' DELIMITER ',' CSV HEADER ;

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas */
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),random(), 'estudiante' 
from tablaEstudiante
where codigo not in (select codigo from personas);

/* Metiendo a la tabla Estudiante */
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre */
insert into semestre(periodo,anio,grupo)
select 1 as periodo,2018 as anio,ga.grupo
from (
	select distinct nombre_asignatura, grupo_asignatura as grupo
	from tablaEstudiante
	order by(nombre_asignatura)
)as ga;

/* Metiendo a la tabla inscrito */
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);

/* Metiendo a la tabla ofrece */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem */
insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select distinct nombre_asignatura
			from tablaEstudiante) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select distinct nombre_asignatura,codigo_asignatura
	from tablaEstudiante
	order by(nombre_asignatura)
) as asig; 

/* Metiendo a la tabla toma */
insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,sem.sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from 
	(tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura) as f1 join
	semestre as sem on sem.sem_id = f1.sem_id
where 
	f1.Grupo_asignatura = sem.grupo AND
	anio = (select max(anio) from semestre) AND
	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre))
order by(codigo);

drop table tablaEstudiante;

-- INSERCION 2018_2 
CREATE TABLE Public.tablaEstudiante(
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
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


COPY Public.tablaEstudiante FROM '/home/felipe/Escritorio/F.G.S/CAPSTON/capstone2020/datos_prueba/Datos_2018_2.csv' DELIMITER ',' CSV HEADER ;

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas */
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),'estudiante', 'estudiante' from tablaEstudiante
where codigo not in (select codigo from personas);

/* Metiendo a la tabla Estudiante */
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre */
insert into semestre(periodo,anio,grupo)
select 2 as periodo,2018 as anio,ga.grupo
from (
	select distinct nombre_asignatura, grupo_asignatura as grupo
	from tablaEstudiante
	order by(nombre_asignatura)
)as ga;

/* Metiendo a la tabla inscrito */
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);

/* Metiendo a la tabla ofrece */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem */
insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select distinct nombre_asignatura
			from tablaEstudiante) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select distinct nombre_asignatura,codigo_asignatura
	from tablaEstudiante
	order by(nombre_asignatura)
) as asig; 

/* Metiendo a la tabla toma */
insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,sem.sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from 
	(tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura) as f1 join
	semestre as sem on sem.sem_id = f1.sem_id
where 
	f1.Grupo_asignatura = sem.grupo AND
	anio = (select max(anio) from semestre) AND
	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre))
order by(codigo);

drop table tablaEstudiante;

-- INSERCION 2019_1
CREATE TABLE Public.tablaEstudiante(
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
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


COPY Public.tablaEstudiante FROM '{}' DELIMITER ',' CSV HEADER ;

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas */
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),'estudiante', 'estudiante' from tablaEstudiante
where codigo not in (select codigo from personas);

/* Metiendo a la tabla Estudiante */
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre */
insert into semestre(periodo,anio,grupo)
select 1 as periodo,2019 as anio,ga.grupo
from (
	select distinct nombre_asignatura, grupo_asignatura as grupo
	from tablaEstudiante
	order by(nombre_asignatura)
)as ga;

/* Metiendo a la tabla inscrito */
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);

/* Metiendo a la tabla ofrece */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem */
insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select distinct nombre_asignatura
			from tablaEstudiante) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select distinct nombre_asignatura,codigo_asignatura
	from tablaEstudiante
	order by(nombre_asignatura)
) as asig; 

/* Metiendo a la tabla toma */
insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,sem.sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from 
	(tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura) as f1 join
	semestre as sem on sem.sem_id = f1.sem_id
where 
	f1.Grupo_asignatura = sem.grupo AND
	anio = (select max(anio) from semestre) AND
	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre))
order by(codigo);

drop table tablaEstudiante;

-- INSERCION 2019_2 
CREATE TABLE Public.tablaEstudiante(
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
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


COPY Public.tablaEstudiante FROM '/home/felipe/Escritorio/F.G.S/CAPSTON/capstone2020/datos_prueba/Datos_2019_2.csv' DELIMITER ',' CSV HEADER ;

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas */
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),'estudiante', 'estudiante' from tablaEstudiante
where codigo not in (select codigo from personas);

/* Metiendo a la tabla Estudiante */
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre */
insert into semestre(periodo,anio,grupo)
select 2 as periodo,2019 as anio,ga.grupo
from (
	select distinct nombre_asignatura, grupo_asignatura as grupo
	from tablaEstudiante
	order by(nombre_asignatura)
)as ga;

/* Metiendo a la tabla inscrito */
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);

/* Metiendo a la tabla ofrece */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem */
insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select distinct nombre_asignatura
			from tablaEstudiante) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select distinct nombre_asignatura,codigo_asignatura
	from tablaEstudiante
	order by(nombre_asignatura)
) as asig; 

/* Metiendo a la tabla toma */
insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,sem.sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from 
	(tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura) as f1 join
	semestre as sem on sem.sem_id = f1.sem_id
where 
	f1.Grupo_asignatura = sem.grupo AND
	anio = (select max(anio) from semestre) AND
	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre))
order by(codigo);

drop table tablaEstudiante;

-- INSERCION 2020_1
CREATE TABLE Public.tablaEstudiante(
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
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


COPY Public.tablaEstudiante FROM '/home/felipe/Escritorio/F.G.S/CAPSTON/capstone2020/datos_prueba/Datos_2020_1.csv' DELIMITER ',' CSV HEADER ;

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas */
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),'estudiante', 'estudiante' from tablaEstudiante
where codigo not in (select codigo from personas);

/* Metiendo a la tabla Estudiante */
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre */
insert into semestre(periodo,anio,grupo)
select 1 as periodo,2020 as anio,ga.grupo
from (
	select distinct nombre_asignatura, grupo_asignatura as grupo
	from tablaEstudiante
	order by(nombre_asignatura)
)as ga;

/* Metiendo a la tabla inscrito */
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);

/* Metiendo a la tabla ofrece */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem */
insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select distinct nombre_asignatura
			from tablaEstudiante) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select distinct nombre_asignatura,codigo_asignatura
	from tablaEstudiante
	order by(nombre_asignatura)
) as asig; 

/* Metiendo a la tabla toma */
insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,sem.sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from 
	(tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura) as f1 join
	semestre as sem on sem.sem_id = f1.sem_id
where 
	f1.Grupo_asignatura = sem.grupo AND
	anio = (select max(anio) from semestre) AND
	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre))
order by(codigo);

drop table tablaEstudiante;

-- INSERCION 2020_2 
CREATE TABLE Public.tablaEstudiante(
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
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


COPY Public.tablaEstudiante FROM '/home/felipe/Escritorio/F.G.S/CAPSTON/capstone2020/datos_prueba/Datos_2020_2.csv' DELIMITER ',' CSV HEADER ;

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas */
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),'estudiante', 'estudiante' from tablaEstudiante
where codigo not in (select codigo from personas);

/* Metiendo a la tabla Estudiante */
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre */
insert into semestre(periodo,anio,grupo)
select 2 as periodo,2020 as anio,ga.grupo
from (
	select distinct nombre_asignatura, grupo_asignatura as grupo
	from tablaEstudiante
	order by(nombre_asignatura)
)as ga;

/* Metiendo a la tabla inscrito */
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);

/* Metiendo a la tabla ofrece */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem */
insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select distinct nombre_asignatura
			from tablaEstudiante) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select distinct nombre_asignatura,codigo_asignatura
	from tablaEstudiante
	order by(nombre_asignatura)
) as asig; 

/* Metiendo a la tabla toma */
insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,sem.sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from 
	(tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura) as f1 join
	semestre as sem on sem.sem_id = f1.sem_id
where 
	f1.Grupo_asignatura = sem.grupo AND
	anio = (select max(anio) from semestre) AND
	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre))
order by(codigo);

drop table tablaEstudiante;

