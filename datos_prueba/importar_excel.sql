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
  ,Codigo_Asignatura     VARCHAR  NOT NULL
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

CREATE TABLE Public.tablaEmpleado(
	Codigo_empleado Integer NOT NULL,
	Nombres_empleado VARCHAR(100) NOT NULL,
	Apellido_1_empleado VARCHAR(100) NOT NULL,
	Apellido_2_empleado VARCHAR(100) NOT NULL,
	correo_institucional VARCHAR(100) NOT NULL,
	sexo VARCHAR(10) NOT NULL,
	Documento_actual VARCHAR(100) NOT NULL,
	esProfesor bool NOT NULL,
	esAdmin bool NOT NULL
);

CREATE TABLE Public.tablaProfesores(
	nombre_completo VARCHAR(100) NOT NULL,
	correo VARCHAR(100) NOT NULL,
	nombre_asignatura VARCHAR(100) NOT NULL,
	grupo INTEGER NOT NULL,
	usuario VARCHAR(100) NOT NULL
);

COPY Public.tablaEstudiante FROM 'C:/Users/juank/Desktop/capstone2020/datos_prueba/Datos_prueba.csv' DELIMITER ',' CSV HEADER ;
COPY Public.tablaEmpleado FROM 'C:\Users\juank\Desktop\capstone2020\datos_prueba\informacion_profesores.csv' DELIMITER ',' CSV HEADER;
COPY Public.tablaProfesores FROM 'C:\Users\juank\Desktop\capstone2020\datos_prueba\Datos_profesores.csv' DELIMITER ',' CSV HEADER;

/* Conjuntos de entidades */

Create table Programa(
	 codigo_programa Integer NOT NULL
	,programa VARCHAR(100) NOT NULL
	,facultad_o_escuela VARCHAR(100) NOT NULL
	, PRIMARY KEY(codigo_programa)
);

create table Personas(
	codigo Integer NOT NULL,
	nombre VARCHAR(100) NOT NULL,
	apellido_1 VARCHAR(100) NOT NULL,
	apellido_2 VARCHAR(100) NOT NULL,
	correo_institucional VARCHAR(100) NOT NULL,
	sexo VARCHAR(10) NOT NULL,
	documento_actual VARCHAR(100) NOT NULL,
	usuario VARCHAR(100) NOT NULL,
	contrasena VARCHAR(100) NOT NULL,
	tipo VARCHAR(50) NOT NULL,
	primary key(codigo)
);

Create table Estudiante(
	codigo Integer NOT NULL,
	documento_ingreso Integer NOT NULL,
	acceso VARCHAR(100) NOT NULL,
	subacceso VARCHAR(100) NOT NULL,
	PRIMARY KEY(codigo),
	FOREIGN KEY (codigo) references Personas
);

create table Empleado(
	codigo Integer NOT NULL,
	esProfesor bool NOT NULL,
	esAdmin bool NOT NULL,
	PRIMARY KEY(codigo),
	FOREIGN KEY (codigo) references Personas
);

Create table Asignaturas(
	codigo_asignatura VARCHAR(100) NOT NULL,
	nombre_asignatura VARCHAR(100) NOT NULL,
	creditos_asignatura NUMERIC NOT NULL,
	tipologia_asignatura VARCHAR(100) NOT NULL,
	porcentaje1 NUMERIC NOT NULL,
	porcentaje2 NUMERIC NOT NULL,
	porcentaje3 NUMERIC NOT NULL,
	porcentaje4 NUMERIC NOT NULL,
	porcentaje5 NUMERIC NOT NULL,
	PRIMARY KEY(codigo_asignatura)
);

create table semestre (
	sem_id serial,
	periodo numeric,
	anio numeric,
	grupo numeric,
	primary key(sem_id)
);

/* Conjuntos de relaciones */

create table ofrece(
	codigo_asignatura VARCHAR(100) NOT NULL,
	codigo_programa Integer NOT NULL,
	PRIMARY KEY (codigo_asignatura),
	FOREIGN KEY (codigo_asignatura) references Asignaturas,
	FOREIGN KEY (codigo_programa) references Programa
);

create table Pertenece(
	codigo Integer NOT NULL,
	codigo_programa Integer NOT NULL,
	PRIMARY KEY (codigo),
	FOREIGN KEY (codigo) references Empleado,
	FOREIGN KEY (codigo_programa) references Programa
);

create table inscrito(
	codigo Integer NOT NULL,
	codigo_programa Integer NOT NULL,
	PRIMARY KEY (codigo),
	FOREIGN KEY (codigo) references Estudiante,
	FOREIGN KEY (codigo_programa) references Programa
);

create table dicta (
	codigo Integer not null,
	sem_id serial not null,
	primary key(codigo,sem_id),
	foreign key (codigo) references Empleado,
	foreign key (sem_id) references semestre
);

create table toma (
	codigo Integer not null,
	sem_id serial not null,
	nota1 numeric not null,
	nota2 numeric not null,
	nota3 numeric not null,
	nota4 numeric not null,
	nota5 numeric not null,
	primary key(codigo,sem_id),
	foreign key (codigo) references Estudiante,
	foreign key (sem_id) references semestre
);

create table curso_sem (
	codigo_asignatura VARCHAR(100) NOT NULL,
	sem_id serial NOT NULL,
	primary key(sem_id),
	foreign key (codigo_asignatura) references Asignaturas,
	foreign key (sem_id) references semestre
);

/* Metiendo a la tabla de Programa */
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela from tablaEstudiante;

/* Metiendo a la tabla de Personas */

insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),'estudiante', 'estudiante' from tablaEstudiante;

insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct Codigo_empleado,Nombres_empleado,Apellido_1_empleado,Apellido_2_empleado,correo_institucional,sexo,Documento_actual, substring(correo_institucional from '(.*)@'),'administrador', 'administrador' 
from tablaEmpleado
where esAdmin='1';

insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct Codigo_empleado,Nombres_empleado,Apellido_1_empleado,Apellido_2_empleado,correo_institucional,sexo,Documento_actual, substring(correo_institucional from '(.*)@'),'profesor', 'profesor' 
from tablaEmpleado
where esAdmin='0';

/* Metiendo a la tabla de Estudiante */

insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso from tablaEstudiante;

/* Metiendo a la tabla Empleado */

insert into Empleado(codigo,esProfesor,esAdmin)
select distinct Codigo_empleado,esProfesor,esAdmin from tablaEmpleado;

/* Metiendo a la tabla de Asignaturas*/

insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p from tablaEstudiante;

/* Metiendo a la tabla de Semestre*/

insert into semestre(periodo,anio,grupo)
select 2 as periodo,2020 as anio,ga.grupo
from (
	select nombre_asignatura,grupo 
	from personas join (
		select codigo_asignatura,asignaturas.nombre_asignatura,grupo,usuario 
		from asignaturas join tablaProfesores on asignaturas.nombre_asignatura = tablaProfesores.nombre_asignatura
	)as B
	on personas.usuario = B.usuario
)as ga;

/* Metiendo a la tabla dicta */

insert into dicta(codigo,sem_id)
select distinct asig.codigo,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select personas.codigo,personas.usuario,codigo_asignatura,nombre_asignatura,grupo 
			from personas join (
				select codigo_asignatura,asignaturas.nombre_asignatura,grupo,usuario 
				from asignaturas join tablaProfesores on asignaturas.nombre_asignatura = tablaProfesores.nombre_asignatura
			)as B
			on personas.usuario = B.usuario) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select codigo,nombre_asignatura
	from personas join (
		select codigo_asignatura,asignaturas.nombre_asignatura,grupo,usuario 
		from asignaturas join tablaProfesores on asignaturas.nombre_asignatura = tablaProfesores.nombre_asignatura
	)as B
	on personas.usuario = B.usuario
) as asig; 

/* Metiendo a la tabla curso_sem */

insert into curso_sem(codigo_asignatura,sem_id)
select distinct asig.codigo_asignatura,(
	select max(sem_id) - ( 
		select count(nombre_asignatura) 
		from(
			select personas.codigo,personas.usuario,codigo_asignatura,nombre_asignatura,grupo 
			from personas join (
				select codigo_asignatura,asignaturas.nombre_asignatura,grupo,usuario 
				from asignaturas join tablaProfesores on asignaturas.nombre_asignatura = tablaProfesores.nombre_asignatura
			)as B
			on personas.usuario = B.usuario) as B
	)
	from semestre
)+row_number() over(order by asig.nombre_asignatura asc) as sem_id
from (
	select nombre_asignatura,codigo_asignatura
	from personas join (
		select codigo_asignatura,asignaturas.nombre_asignatura,grupo,usuario 
		from asignaturas join tablaProfesores on asignaturas.nombre_asignatura = tablaProfesores.nombre_asignatura
	)as B
	on personas.usuario = B.usuario
) as asig; 

/* Metiendo a la tabla inscrito */

insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa;

/* Metiendo a la tabla ofrece */

insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa;

/* Metiendo a la tabla pertenece */

insert into pertenece(codigo,codigo_programa)
select distinct codigo,1 as codigo_programa
from tablaProfesores as tp join personas on tp.usuario = personas.usuario;

/* Metiendo a la tabla toma */

insert into toma(codigo,sem_id,nota1,nota2,nota3,nota4,nota5)

select distinct codigo,sem_id,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from tablaEstudiante as te join curso_sem as cs on te.codigo_asignatura = cs.codigo_asignatura;

drop table tablaEstudiante;
drop table tablaEmpleado;
drop table tablaProfesores;

-- VISTA ayuda en consultas 

CREATE VIEW RESUMEN AS
SELECT Bc.codigo as est_cod,Bc.nombre as nombre_est,Bc.usuario as est_usr,Bc.apellido_1 as ap1_est, Bc.apellido_2 as ap2_est, Bc.correo_institucional as est_mail,Bc.documento_actual as est_id,Bc.sexo as est_sex,Bc.sem_id,Bd.porcentaje1,nota1,Bd.porcentaje2,nota2,Bd.porcentaje3,nota3,Bd.porcentaje4,nota4,Bd.porcentaje5,nota5,Bd.codigo as prof_cod, Bd.nombre as nombre_prof,Bd.usuario as prof_usr,Bd.apellido_1 as ap1_prof ,Bd.apellido_2 as ap2_prof,Bd.correo_institucional as prof_mail, Bd.sexo as prof_sex, Bd.documento_actual as prof_id,Bd.codigo_asignatura,Bd.nombre_asignatura, Bd.creditos_asignatura, periodo,anio,grupo
FROM
	(select * from Personas natural join toma) as Bc join
	(select B1.codigo, nombre,usuario,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,B2.sem_id,codigo_asignatura,nombre_asignatura,creditos_asignatura,periodo,anio,grupo,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5
	 FROM
		(select Personas.codigo,nombre,usuario,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,sem_id
		 from Personas join
		 dicta on Personas.codigo = dicta.codigo ) as B1 join
		(select codigo_asignatura,nombre_asignatura,creditos_asignatura,semestre.sem_id,periodo,anio,grupo,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5
		 FROM
			(select Asignaturas.codigo_asignatura, nombre_asignatura,creditos_asignatura,sem_id,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5
			FROM
				Asignaturas join curso_sem on Asignaturas.codigo_asignatura =  curso_sem.codigo_asignatura ) as B join
				semestre on B.sem_id = semestre.sem_id) as B2
	on B1.sem_id = B2.sem_id) as Bd
	on Bc.sem_id = Bd.sem_id;
	
