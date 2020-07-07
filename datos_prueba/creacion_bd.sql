
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

-- Creacion tabla para manejar las alertas
create table alertas (
	usuario VARCHAR(100) NOT NULL,
	texto TEXT NOT NULL,
	tipo VARCHAR(100) NOT NULL,
	fecha TIMESTAMP NOT NULL,
	periodo numeric NOT NULL,
	anio numeric NOT NULL,
	nombre_asignatura VARCHAR(100),
	visto_estudiante bool NOT NULL DEFAULT FALSE,
	visto_admin bool NOT NULL DEFAULT FALSE,
	oculto_estudiante bool NOT NULL DEFAULT FALSE,
	oculto_admin bool NOT NULL DEFAULT FALSE
);

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
