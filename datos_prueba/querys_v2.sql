-------- Querys --------
-- Query consulta asignaturas y notas de un estudiante
SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5
FROM RESUMEN
WHERE 
	est_usr = 'juanita.gomez' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura);

-- Query consulta asignaturas y porcentaje notas de un estudiante
SELECT nombre_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5
FROM RESUMEN
WHERE 
	est_usr = 'myacusbw' AND -- USUARIO DEL ESTUDIANTE QUE HIZO LOGIN
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura);

-- Query consulta asignaturas dadas por un profesor
SELECT DISTINCT nombre_asignatura
FROM RESUMEN
WHERE
	prof_usr = 'margot.salas' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura)	
	
-- Query consulta estudiantes y notas por materia y profesor 
SELECT nombre_est,ap1_est,ap2_est,est_usr,nota1,nota2,nota3,nota4,nota5
FROM RESUMEN 
WHERE
	prof_usr = 'alexander.caicedo' AND -- USUARIO DEL PROFESOR QUE HIZO LOGIN
	nombre_asignatura = 'Algebra lineal' AND -- MATERIA SELECCIONADA
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_est)

-- Query consulta de todas las asignaturas,codigo,creditos,grupos,porcentajes y profesor.
SELECT distinct nombre_asignatura,codigo_asignatura,creditos_asignatura,grupo,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5,nombre_prof
FROM RESUMEN
WHERE
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura);

-- UPDATE para las notas de los estudiantes.
UPDATE toma
SET -- Las 'nueva nota' se reemplazan por la nueva nota NUMERICA NO STRING
	nota1 = 5.0,
	nota2 = 5.0,
	nota3 = 5.0,
	nota4 = 5.0,
	nota5 = 5.0
WHERE	
	codigo_asignatura = (select distinct codigo_asignatura from RESUMEN where nombre_asignatura = 'Cornerstone project') AND
	codigo = (select distinct est_cod from RESUMEN where est_usr = 'felipe.guzman') AND 
	grupo = (
		select distinct grupo
		from RESUMEN
		where 
			prof_usr = 'alexander.caicedo' AND
			nombre_asignatura = 'Cornerstone project' AND
			anio = (select max(anio) from RESUMEN) AND
			periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
	) AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN));


-- Query consulta grupos de una materia seleccionada 
SELECT distinct nombre_asignatura,grupo,prof_usr, nombre_prof,ap1_prof,ap2_prof
FROM RESUMEN 
WHERE 
	nombre_asignatura = 'Algebra lineal' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(grupo);

-- Query promedios por cohorte para un estudiante

SELECT 
	round(sum(creditos_asignatura*nota1)/sum(creditos_asignatura),2) as promedio_cohorte1,
	round(sum(creditos_asignatura*nota2)/sum(creditos_asignatura),2) as promedio_cohorte2,
	round(sum(creditos_asignatura*nota3)/sum(creditos_asignatura),2) as promedio_cohorte3,
	round(sum(creditos_asignatura*nota4)/sum(creditos_asignatura),2) as promedio_cohorte4,
	round(sum(creditos_asignatura*nota5)/sum(creditos_asignatura),2) as promedio_cohorte5,
	round(sum(creditos_asignatura*round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+porcentaje5*nota5)/100,2))/sum(creditos_asignatura),2) as promedio_semestral
FROM RESUMEN
WHERE
	est_usr = 'daniel.felipe' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN));
	
-- Query semestres en los que estudiante inscribio asignaturas.
SELECT distinct cast(anio as varchar)||'-'||cast(periodo as varchar)
FROM resumen
WHERE est_usr = 'juanc.llanos';

-- Query semestres en los que profesor dicto asignaturas.
SELECT distinct cast(anio as varchar)||'-'||cast(periodo as varchar)
FROM resumen
WHERE prof_usr = 'margot.salas';

-- Query consulta asignaturas y notas de un estudiante en un periodo y anio especifico
SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5
FROM RESUMEN
WHERE 
	est_usr = 'juanita.gomez' AND
	anio = 2019 AND
	periodo = 2
ORDER BY(nombre_asignatura);

-- Query consulta asignaturas dadas por un profesor en un periodo y anio especifico
SELECT DISTINCT nombre_asignatura
FROM RESUMEN
WHERE
	prof_usr = 'margot.salas' AND
	anio = 2018 AND
	periodo = 2
ORDER BY(nombre_asignatura)	

-- Query consulta todas las alertas 

SELECT nombre,apellido_1,apellido_2,texto,alertas.tipo as alerta,fecha,periodo,anio,nombre_asignatura
FROM alertas join personas on alertas.usuario = personas.usuario;

-- Query consulta numero de alertas por estudiante dado el usuario no leidas

SELECT count(*)
FROM alertas
WHERE 
	usuario = 'juanc.llanos' AND
	visto_estudiante = '0';

-- Query consulta cantidad de alertas no leidas

SELECT count(*)
FROM alertas
WHERE visto_admin = '0';

-- Query promedio acumulado de un estudiante dado su usuario

SELECT round(sum(creditos_asignatura*(nota1*porcentaje1+nota2*porcentaje2+nota3*porcentaje3+nota4*porcentaje4+nota5*porcentaje5)/100)/sum(creditos_asignatura),2) 
FROM RESUMEN
WHERE est_usr = 'juanita.gomez';

-- Query periodo academico, promedio por periodo y creditos inscritos

SELECT 
	distinct cast(anio as varchar)||'-'||cast(periodo as varchar),
	round(sum(creditos_asignatura*(nota1*porcentaje1+nota2*porcentaje2+nota3*porcentaje3+nota4*porcentaje4+nota5*porcentaje5)/100)/sum(creditos_asignatura),2),
	sum(creditos_asignatura)
FROM RESUMEN
WHERE est_usr = 'juanita.gomez'
GROUP BY(anio,periodo);

-- Promedio general 
select round(avg(promedios),2) from
(select round((porcentaje1*nota1 +porcentaje2*nota2 + porcentaje3*nota3 + porcentaje4*nota4 + porcentaje5*nota5)/100,2) as promedios, est_usr
from resumen 
where nombre_asignatura = 'Precalculo') as B;

-- Porcentaje reprobados
select round(cast(count(promedios) as numeric)/cast((select count(*) from resumen where nombre_asignatura = 'Precalculo') as numeric),2) * 100 as porc_aprobados from
(select round((porcentaje1*nota1 +porcentaje2*nota2 + porcentaje3*nota3 + porcentaje4*nota4 + porcentaje5*nota5)/100,2) as promedios, est_usr
from resumen 
where nombre_asignatura = 'Precalculo') as B
where promedios<3;

-- Nota minima y maxima
select min(promedios) as minimo, max(promedios) as maximo from
(select round((porcentaje1*nota1 +porcentaje2*nota2 + porcentaje3*nota3 + porcentaje4*nota4 + porcentaje5*nota5)/100,2) as promedios, est_usr
from resumen 
where nombre_asignatura = 'Precalculo') as B;



	
