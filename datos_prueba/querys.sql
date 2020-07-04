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
	nota1 = 0.0,
	nota2 = 0.5,
	nota3 = 0.7,
	nota4 = 0.9,
	nota5 = 0.0
WHERE	
	toma.sem_id = (
		select sem_id
		from RESUMEN
		where 
			prof_usr = 'mauro.artigiani' AND -- USUARIO DEL PROFESOR QUE HIZO LOGIN
			nombre_asignatura = 'Algebra lineal' AND -- MATERIA SELECCIONADA
			RESUMEN.est_usr = 'rsoykrea' AND -- USUARIO DEL ESTUDIANTE A CAMBIAR NOTAS
			anio = (select max(anio) from RESUMEN) AND
			periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
	) AND 
	toma.codigo = (
		select distinct est_cod
		from RESUMEN
		where
			est_usr = 'rsoykrea'
	);
	
select * from resumen;


-- Query consulta grupos de una materia seleccionada 
SELECT distinct nombre_asignatura,grupo,prof_usr, nombre_prof,ap1_prof,ap2_prof
FROM RESUMEN 
WHERE 
	nombre_asignatura = 'Algebra lineal' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(grupo);

-- Query promedios por cohorte para un estudiante

select 
	round(sum(creditos_asignatura*nota1)/sum(creditos_asignatura),2) as promedio_cohorte1,
	round(sum(creditos_asignatura*nota2)/sum(creditos_asignatura),2) as promedio_cohorte2,
	round(sum(creditos_asignatura*nota3)/sum(creditos_asignatura),2) as promedio_cohorte3,
	round(sum(creditos_asignatura*nota4)/sum(creditos_asignatura),2) as promedio_cohorte4,
	round(sum(creditos_asignatura*nota5)/sum(creditos_asignatura),2) as promedio_cohorte5,
	round(sum(creditos_asignatura*round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+porcentaje5*nota5)/100,2))/sum(creditos_asignatura),2) as promedio_semestral
from RESUMEN
where
	est_usr = 'daniel.felipe' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN));
	
-- Query semestres en los que estudiante inscribio asignaturas.
select distinct anio,periodo from resumen
where est_usr = 'juanc.llanos'

-- Query semestres en los que profesor dicto asignaturas.
select distinct anio,periodo from resumen
where prof_usr = 'margot.salas'
	
