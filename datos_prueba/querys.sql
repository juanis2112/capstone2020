-- Query consulta asignaturas y notas de un estudiante
SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5
FROM RESUMEN
WHERE 
	est_usr = 'ESTU' AND
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura);

-- Query consulta asignaturas y porcentaje notas de un estudiante
SELECT nombre_asignatura,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5
FROM RESUMEN
WHERE 
	est_usr = 'ESTU' AND -- USUARIO DEL ESTUDIANTE QUE HIZO LOGIN
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura);

-- Query consulta asignaturas dadas por un profesor
SELECT nombre_asignatura
FROM RESUMEN join personas on RESUMEN.prof_cod = personas.codigo
WHERE 
	personas.usuario = 'PROF' AND -- USUARIO DEL PROFESOR QUE HIZO LOGIN
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura)
	
 
-- Query consulta estudiantes y notas por materia y profesor 
SELECT nombre_est,nota1,nota2,nota3,nota4,nota5
FROM RESUMEN join personas on RESUMEN.prof_cod = personas.codigo
WHERE 
	personas.usuario = 'PROF' AND -- USUARIO DEL PROFESOR QUE HIZO LOGIN
	nombre_asignatura = 'Escritura de ensayos de opinion' AND -- MATERIA SELECCIONADA
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_est);

-- Query consulta de todas las asignaturas,codigo,creditos,grupos,porcentajes y profesor.
SELECT nombre_asignatura,codigo_asignatura,creditos_asignatura,grupo,porcentaje1,porcentaje2,porcentaje3,porcentaje4,porcentaje5,nombre_prof
FROM RESUMEN
WHERE
	anio = (select max(anio) from RESUMEN) AND
	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
ORDER BY(nombre_asignatura);


