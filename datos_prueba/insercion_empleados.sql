-- Insercion de datos de empleados.

/* Creamos tablaEmpleado para almacenar toda la informacion del excel, aqui obtenemos el codigo de este empleado,
	sus nombre, primer apellido, segundo appelido, correo, sexo, documento, y dos columnas que nos permiten saber
	que rol o roles desempeña, puede ser profesor, administrador o ambas.
*/
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

/* Con esta instruccion llenamos de informacion tablaEmpleado con lo que hay en el excel*/
COPY Public.tablaEmpleado FROM '{path}' DELIMITER ',' CSV HEADER;

/*  Metiendo a la tabla Personas 
	En esta parte lo que se hace es ingresar en personas la informacion de los empleados son admin primero, se revisa tambien que este no haya sido guardado
	de manera previa.
*/
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct Codigo_empleado,Nombres_empleado,Apellido_1_empleado,Apellido_2_empleado,correo_institucional,sexo,Documento_actual, substring(correo_institucional from '(.*)@'),crypt(cast(Codigo_empleado as text) , gen_salt('xdes')), 'administrador' 
from tablaEmpleado
where 
	esAdmin='1' and
	Codigo_empleado not in (select codigo from personas);


/* Metiendo a la tabla Personas 
	Luego lo que se hace es ingresar toda la informacion en Personas de quienes no son administradores ademas se revisa que no haya sido registrado previamente.
*/

insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct Codigo_empleado,Nombres_empleado,Apellido_1_empleado,Apellido_2_empleado,correo_institucional,sexo,Documento_actual, substring(correo_institucional from '(.*)@'),crypt(cast(Codigo_empleado as text) , gen_salt('xdes')), 'profesor' 
from tablaEmpleado
where 
	esAdmin='0' and 
	Codigo_empleado not in (select codigo from personas);

/* Metiendo a la tabla Empleado 
	En esta parte lo que se hace es ingresar el registro de cada usuario con el perfil de empleado 
	(profesor o administrativo) en su respectiva tabla del modelo. Esto se hace posterior a crear el 
	usuario en la tabla personas.
*/
insert into Empleado(codigo,esProfesor,esAdmin)
select distinct Codigo_empleado,esProfesor,esAdmin 
from tablaEmpleado
where codigo_empleado not in (select codigo from empleado);

drop table tablaEmpleado;