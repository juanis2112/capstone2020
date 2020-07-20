-- Insercion cursos de un periodo academico.


/* tablaProfesores se usa para manejar la informacion de que profesor dicta que asignatura y que grupo.*/
CREATE TABLE Public.tablaProfesores(
	nombre_completo VARCHAR(100) NOT NULL,
	correo VARCHAR(100) NOT NULL,
	nombre_asignatura VARCHAR(100) NOT NULL,
	grupo INTEGER NOT NULL,
	usuario VARCHAR(100) NOT NULL
);

/* Esta instruccion nos sirve para copiar en tablaProfesores toda la informacion del excel.*/
COPY Public.tablaProfesores FROM '{path}' DELIMITER ',' CSV HEADER;


/* Metiendo a la tabla dicta.
	En esta parte lo que se hace es asignar a cada profesor una clase del semestre el cual ya tiene una asignatura
	determinada. 
*/
insert into dicta(codigo,codigo_asignatura,periodo,anio,grupo)
select codigo,codigo_asignatura,{period},{year},grupo from 
(select * from tablaProfesores join asignaturas on tablaProfesores.nombre_asignatura = asignaturas.nombre_asignatura) as B join personas
on B.usuario = personas.usuario;


/* Metiendo a la tabla pertenece 

	En esta parte lo que se hace es asignar un porgrama a cada asignatura. Para la aplicación todas las asignaturas
	pertenecen al programa MACC

*/
insert into pertenece(codigo,codigo_programa)
select distinct codigo,1 as codigo_programa
from tablaProfesores as tp join personas on tp.usuario = personas.usuario
where codigo not in (select codigo from pertenece);

/* Cuando ya usamos toda la informacion necesaria borramos la tabla de apoyo tablaProfesores*/
drop table tablaProfesores;


