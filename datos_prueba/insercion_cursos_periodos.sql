
CREATE TABLE Public.tablaProfesores(
	nombre_completo VARCHAR(100) NOT NULL,
	correo VARCHAR(100) NOT NULL,
	nombre_asignatura VARCHAR(100) NOT NULL,
	grupo INTEGER NOT NULL,
	usuario VARCHAR(100) NOT NULL
);

COPY Public.tablaProfesores FROM '{path}' DELIMITER ',' CSV HEADER;

-- Metiendo a la tabla dicta.
insert into dicta(codigo,codigo_asignatura,periodo,anio,grupo)
select codigo,codigo_asignatura,{period},{year},grupo from 
(select * from tablaProfesores join asignaturas on tablaProfesores.nombre_asignatura = asignaturas.nombre_asignatura) as B join personas
on B.usuario = personas.usuario;
-- Cambiar 1 & 2018 por el periodo y anio correspondiente.

/* Metiendo a la tabla pertenece */
insert into pertenece(codigo,codigo_programa)
select distinct codigo,1 as codigo_programa
from tablaProfesores as tp join personas on tp.usuario = personas.usuario
where codigo not in (select codigo from pertenece);

drop table tablaProfesores;


