-- Insercion de estudiantes y asignaturas.

/* Archivo que nos permite tener un formato de instrucciones de SQL para ingresar la informacion de los estudiantes */

/*
  tablaEstudiante nos permite tener almacenada de manera temporal la informacion que se encuentra en el Excel que relaciona
  estudiantes con las asignaturas.
*/
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
  ,Codigo_Asignatura     VARCHAR(100)  NOT NULL
  ,Nombre_Asignatura     VARCHAR(100) NOT NULL
  ,Creditos_Asignatura   INTEGER  NOT NULL
  ,Grupo_Asignatura      INTEGER  NOT NULL
  ,Tipologia_Asignatura  VARCHAR(100) NOT NULL
  ,Nota_1er_Corte        NUMERIC(3,1) 
  ,Corte_1p              INTEGER  NOT NULL
  ,Nota_2do_Corte        NUMERIC(3,1) 
  ,Corte_2p              INTEGER  NOT NULL
  ,Nota_3er_Corte        NUMERIC(3,1) 
  ,Corte_3p              INTEGER  NOT NULL
  ,Nota_4to_Corte        NUMERIC(3,1) 
  ,Corte_4p              INTEGER  NOT NULL
  ,Nota_5to_Corte        NUMERIC(3,1) 
  ,Corte_5p              INTEGER  NOT NULL
	, PRIMARY KEY(Documento_actual,Nombre_Asignatura)
);

/*Aqui se copia en esta tabla todo la informacion del excel*/
COPY Public.tablaEstudiante FROM '{path}' DELIMITER ',' CSV HEADER ;


/* -- Metiendo a la tabla de Programa --
  En este apartado ingresamos a la tabla Programa los distintos programas, como nos limitamos solamente a MACC
  el unico codigo es 1 y corresponde a este programa.
*/
insert into Programa(codigo_programa,programa,facultad_o_escuela) 
select distinct 1,programa, facultad_o_escuela 
from tablaEstudiante
where 1 not in (select codigo_programa from programa);

/* Metiendo a la tabla de Personas 
  En esta insercion ingresamos a la tabla Personas toda la informacion que nos brindan de los estudiantes, seleccionamos distintos
  ya que un mismo estudiante puede ver varias asignaturas por lo que se debe elegir solo una vez su informacion y se revisa que esta
  informacion no haya sido introducida anteriormente para no volerlos ingresar.
*/
insert into Personas(codigo,nombre,apellido_1,apellido_2,correo_institucional,sexo,documento_actual,usuario,contrasena, tipo)
select distinct codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual, substring(correo_institucional from '(.*)@'),crypt(cast(codigo as text) , gen_salt('xdes')), 'estudiante' 
from tablaEstudiante
where codigo not in (select codigo from personas)
group by(codigo,nombres_estudiante,apellido_1_estudiante,apellido_2_estudiante,correo_institucional,sexo,documento_actual);

/* Metiendo a la tabla Estudiante 
  En la especializacion Estudiante ingresamos la informacion que se quiere tener de los estudiantes como su acceso y subacceso entre 
  otros campos, revisamos de nuevo que esta informacion no haya sido previamente guardada.
*/
insert into Estudiante(codigo,documento_ingreso,acceso,subacceso)
select distinct codigo,documento_ingreso,acceso,subacceso 
from tablaEstudiante
where codigo not in (select codigo from estudiante);

/* Metiendo a la tabla de Asignaturas
  En la tabla de Asignaturas guardamos toda la informacion de las asignaturas que registraron los estudiantes, tambien revisamos que esta 
  no haya sido previamente almacenada.
*/
insert into Asignaturas(codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5)
select distinct codigo_asignatura,nombre_asignatura,creditos_asignatura,tipologia_asignatura,Corte_1p,Corte_2p,Corte_3p,Corte_4p,Corte_5p 
from tablaEstudiante
where codigo_asignatura not in (select codigo_asignatura from asignaturas);

/* Metiendo a la tabla de Semestre 
  En Semestre llevamos un registro de las asignaturas con sus grupos, el periodo y año que fue registrada, esto nos sirve para saber y diferenciar
  tanto grupos por semestre de la misma asignatura como grupos de la asignatura en distintos momentos en el tiempo.
*/
insert into semestre(codigo_asignatura,periodo,anio,grupo)
select distinct codigo_asignatura,{period},{year},Grupo_Asignatura from tablaEstudiante
where (codigo_asignatura,{period},{year},Grupo_Asignatura) not in (select codigo_asignatura,{period},{year},grupo from semestre);

/* Metiendo a la tabla inscrito 
  En este apartado sacamos los estudiantes junto con el programa al que pertenece y lo ingresamos a la relacion inscrito, esto para saber
  a que programa pertenece cada estudiante.
*/
insert into inscrito(codigo,codigo_programa)
select distinct codigo,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo not in (select codigo from inscrito);


/* Metiendo a la tabla ofrece
  En esta relacion mantenemos informacion de a que programa pertenecen las asignaturas, de momento estamos colocando las asignaturas
  en el programa de MACC.
 */
insert into ofrece(codigo_asignatura,codigo_programa)
select distinct  codigo_asignatura,codigo_programa 
from tablaEstudiante as te join programa as pr on te.programa = pr.programa
where codigo_asignatura not in (select codigo_asignatura from ofrece);

/* Metiendo a la tabla curso_sem 
  En curso_sem manejamos la misma informacion que en semestre por lo que aca guardamos el codigo de la asignatura, el periodo, año y grupo
  como comentamos en Semestre. 
*/
insert into curso_sem(codigo_asignatura,periodo,anio,grupo)
select distinct codigo_asignatura,{period},{year},Grupo_Asignatura from tablaEstudiante
where (codigo_asignatura,{period},{year},Grupo_Asignatura) not in (select codigo_asignatura,{period},{year},grupo from curso_sem);

/* Metiendo a la tabla toma
  En esta relacion guardamos la informaicon de los estudiantes con las asignaturas que vio, guardamos tanto los codigos del estudiante como el de
  la asignatura y tambien el grupo, periodo,año y las notas que este estudiante tiene en la asignatura, si no tiene notas registradas simplemente 
  sera vacio.
 */
insert into toma(codigo,codigo_asignatura,periodo,anio,grupo,nota1,nota2,nota3,nota4,nota5)
select distinct codigo,codigo_asignatura,{period},{year},Grupo_Asignatura,Nota_1er_Corte,Nota_2do_Corte,Nota_3er_Corte,Nota_4to_Corte,Nota_5to_Corte
from tablaEstudiante
where (codigo,codigo_asignatura,{period},{year},Grupo_Asignatura) not in (select codigo,codigo_asignatura,{period},{year},grupo from toma);


/*Cuando ya sacamos toda la informacion de este archivo de excel simplemente borramos tablaEstudiante */
drop table tablaEstudiante;
