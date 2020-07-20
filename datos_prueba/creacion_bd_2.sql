CREATE EXTENSION pgcrypto;

/*  Archivo para crear todas las tablas (asociadas al modelo entidad relacion y otros aspectos) necesarias para el uso de la base de datos. 
	Cada tabla representa lo siguiente:

	--> Programa: Almacena las carreras que ofrece la universidad. Para esta aplicación la inserción se limita a 
				solo una carrera.
	--> Personas: Almacena la información de todos los usuarios que interactuan con la aplicación sin importar el 
				perfil que tengan. Representa en el modelo entidad relación una generalización de los roles de la aplicacion.
	--> Estudiante: Especialización de la tabla 'Personas'. Almacena a todos los estudiantes que son inscritos en la
				aplicación.
	--> Empleado: Esta tabla almacena la informacion sobre si la persona almacenada cumple el rol de profesor, administrador 
				o ambos.
	--> Asignaturas: Esta tabla nos habla de las asignaturas registradas en la universidad con su respectivo codigo, nombre, 
				numero de creditos, tipologia y porcentaje sobre las distintas cohortes.
	--> semestre: Almacena todas las clases a las que se inscribe un estudiante cada semestre. A cada registro se le 
				asocia una asignatura, un profesor y un conjunto de estudiantes. Además contiene un atributo el cual
				representa el grupo de la asignatura a la cual pertenece la clase.
	--> alertas: Almacena todas las alertas que la aplicación Epsilon genera de forma automática o manual. 
	--> logging: Almacena todas las interacciones se los usuarios con la aplicación. Se divide en acciones como 'CONSULTA'
				'EDICION','IMPORTACION','EXPORTACION','INICIO' y 'SALIDA'.
	--> ofrece: En ofrece podemos encontrar la relacion entre asignaturas y programas académicos, es decir, donde se referencia
				a que programa pertenece una asingatura.
	--> Pertenece: Representa una relación en el modelo entidad relación entre las tablas 
	--> inscrito: En esta tabla se tiene almacenada la relacion de los estudiantes con los programas, aqui podemos saber a que 
				a que programa pertenece un estudiante.
	--> dicta: En esta tabla se llevan los registros de los profesores con las asignaturas, aqui se tiene almacenada la informacion
				de que asignaturas dicto un profesor, en que periodo, en que año y el o los grupos a los que dicto clase.
	--> toma: Esta relacion nos dice que cursos tomaron los estudiantes y se tiene la informacion del periodo en el que se tomo
				(primer semestre, segundo semestre o intersemestral), el año y el grupo al que pertenece o pertenecio el 
				estudiante tambien se tienen las notas en los 5 cohortes del estudiante, ademas las referencias a estudiante y 
				asignatura se dan con los respectivos codigos de estas entidades.
	--> curso_sem:	Esta tabla nos permite saber la relacion entre asignaturas y el momento en el tiempo, aqui almacenamos la asignatura,
				el periodo, el año y el grupo de esta.
	--> notificacion: Es una relacion que implementamos para llevar un registro de los administradores con las alertas, esto para saber
				que admin borro que alerta para no mostrarsela mas sin afectar la visibilidad para los otros administradores.
	--> Resumen: Esta vista simplemente nos ayuda a tener la informacion de manera mas reducida, tiene un par de finalidades. La primera 
				como ya se comento nos permite tener de manera resumida informacion especifica de los estudiantes y cursos, por otro lado
				tambien nos ayuda a limitar la interaccion de la aplicacion con la base de datos para no filtrar informacion innecesaria
				o algun inconveniente de ese estilo
*/

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
	estado_cuenta BOOL NOT NULL DEFAULT TRUE,
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

create table logging(
	usuario VARCHAR(100) NOT NULL,
	nivel Integer NOT NULL,
	accion VARCHAR(100) NOT NULL,
	fecha VARCHAR(100) NOT NULL,
	texto TEXT NOT NULL
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


/*  En esta parte introducimos un usuario principal a la aplicacion el cual sera el primer usuario y con el cual
	se puede llenar de informacion la aplicacion.
*/
INSERT INTO personas VALUES (1,'ADMIN','-','-','admin@urosario.edu.co','-',1,'admin',crypt('admin', gen_salt('xdes')),'administrador');
INSERT INTO Empleado VALUES (1,'0','1');