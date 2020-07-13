
CREATE TABLE Public.tablaProfesores(
	nombre_completo VARCHAR(100) NOT NULL,
	correo VARCHAR(100) NOT NULL,
	nombre_asignatura VARCHAR(100) NOT NULL,
	grupo INTEGER NOT NULL,
	usuario VARCHAR(100) NOT NULL
);

COPY Public.tablaProfesores FROM '{}' DELIMITER ',' CSV HEADER;

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
	order by(nombre_asignatura)
) as asig; 


/* Metiendo a la tabla pertenece */
insert into pertenece(codigo,codigo_programa)
select distinct codigo,1 as codigo_programa
from tablaProfesores as tp join personas on tp.usuario = personas.usuario
where codigo not in (select codigo from pertenece);


drop table tablaEstudiante;
drop table tablaEmpleado;
drop table tablaProfesores;