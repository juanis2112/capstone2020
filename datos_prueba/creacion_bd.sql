
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
