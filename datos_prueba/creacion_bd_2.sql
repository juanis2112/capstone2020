CREATE EXTENSION pgcrypto;

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
    codigo_asignatura varchar(100) not null,
	periodo numeric not null,
	anio numeric not null,
	grupo numeric not null,
	primary key(codigo_asignatura,periodo,anio,grupo),
    FOREIGN KEY(codigo_asignatura) REFERENCES Asignaturas
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
    codigo Integer NOT NULL,
    codigo_asignatura VARCHAR(100) NOT NULL,
	periodo numeric not null,
	anio numeric not null,
	grupo numeric not null,
    PRIMARY KEY (codigo,codigo_asignatura,periodo,anio,grupo),
    foreign key(codigo) REFERENCES Empleado,
    foreign key(codigo_asignatura) REFERENCES Asignaturas
);

create table toma (
    codigo Integer NOT NULL,
    codigo_asignatura VARCHAR(100) NOT NULL,
	periodo numeric not null,
	anio numeric not null,
	grupo numeric not null,
	nota1 numeric ,
	nota2 numeric ,
	nota3 numeric ,
	nota4 numeric ,
	nota5 numeric ,
	PRIMARY KEY (codigo,codigo_asignatura,periodo,anio),
	foreign key (codigo) references Estudiante,
	foreign key (codigo_asignatura) REFERENCES Asignaturas
);

create table curso_sem (
    codigo_asignatura VARCHAR(100) NOT NULL,
	periodo numeric not null,
	anio numeric not null,
	grupo numeric not null,
    PRIMARY KEY (codigo_asignatura,periodo,anio,grupo),
	foreign key (codigo_asignatura) references Asignaturas
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
	oculto_estudiante bool NOT NULL DEFAULT FALSE,
	primary key(usuario,fecha)
);
create table notificacion(
	usuario VARCHAR(100) NOT NULL,
	fecha TIMESTAMP NOT NULL,
	codigo Integer NOT NULL,
	visto_admin bool NOT NULL DEFAULT FALSE,
	oculto_admin bool NOT NULL DEFAULT FALSE,
	foreign key(usuario,fecha) references alertas,
	foreign key(codigo) references empleado,
	primary key(codigo,usuario,fecha)
);
create table loggin(
	usuario VARCHAR(100) NOT NULL,
	accion VARCHAR(100) NOT NULL,
	fecha VARCHAR(100) NOT NULL,
	texto TEXT NOT NULL
);

-- VISTA ayuda en consultas 
create view RESUMEN as
select distinct est_cod,est_usr,nombre_est,ap1_est,ap2_est,B6.codigo_asignatura,creditos_asignatura,nombre_asignatura,B6.grupo,periodo,anio,porcentaje1,nota1,porcentaje2,nota2,porcentaje3,nota3,porcentaje4,nota4,porcentaje5,nota5,prof_cod,prof_usr,nombre_prof,ap1_prof,ap2_prof from
(select distinct codigo as est_cod,usuario as est_usr,nombre_est,ap1_est,ap2_est,B1.codigo_asignatura,nombre_asignatura,creditos_asignatura,B1.grupo,B1.periodo,B1.anio, nota1,nota2,nota3,nota4,nota5,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5 from
((select usuario,codigo,nombre as nombre_est,apellido_1 as ap1_est,apellido_2 as ap2_est from estudiante natural join personas) as B natural join toma ) as B1 join 
(select * from 
(select * from asignaturas natural join curso_sem) as B natural join semestre) as B2
on (B1.codigo_asignatura = B2.codigo_asignatura and B1.grupo = B2.grupo)) as B6
join (select codigo as prof_cod,usuario as prof_usr,nombre_prof,ap1_prof,ap2_prof,codigo_asignatura,grupo from (select codigo,usuario,nombre as nombre_prof,apellido_1 as ap1_prof,apellido_2 as ap2_prof from empleado natural join personas) as B natural join dicta) as B7
on (B6.codigo_asignatura = B7.codigo_asignatura and B6.grupo = B7.grupo);

INSERT INTO personas VALUES (1,'ADMIN','-','-','admin@urosario.edu.co','-',1,'admin',crypt('admin', gen_salt('xdes')),'administrador');
INSERT INTO Empleado VALUES (1,'0','1');