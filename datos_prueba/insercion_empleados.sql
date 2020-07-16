-- Insercion de datos de empleados.

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

COPY Public.tablaEmpleado FROM '{path}' DELIMITER ',' CSV HEADER;

-- Metiendo a la tabla Personas
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct Codigo_empleado,Nombres_empleado,Apellido_1_empleado,Apellido_2_empleado,correo_institucional,sexo,Documento_actual, substring(correo_institucional from '(.*)@'),crypt(cast(Codigo_empleado as text) , gen_salt('xdes')), 'administrador' 
from tablaEmpleado
where 
	esAdmin='1' and
	Codigo_empleado not in (select codigo from personas);

insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct Codigo_empleado,Nombres_empleado,Apellido_1_empleado,Apellido_2_empleado,correo_institucional,sexo,Documento_actual, substring(correo_institucional from '(.*)@'),crypt(cast(Codigo_empleado as text) , gen_salt('xdes')), 'profesor' 
from tablaEmpleado
where 
	esAdmin='0' and 
	Codigo_empleado not in (select codigo from personas);

/* Metiendo a la tabla Empleado */
insert into Empleado(codigo,esProfesor,esAdmin)
select distinct Codigo_empleado,esProfesor,esAdmin 
from tablaEmpleado
where codigo_empleado not in (select codigo from empleado);

drop table tablaEmpleado;