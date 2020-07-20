
# Manuel de Usuario


# Índice

0. Caso base

1.Iniciando sesión. 

2.Estudiante 

a. Ver datos personales. 

b. Ver notas de asignaturas de un periodo académico.  

c. Descargar notas de un periodo académico. 

d. Ver y borrar alertas 

3. Profesor 

- a. Ver materias dictadas de un periodo académico. 

- b. Ver estudiantes y notas de una asignatura dictada. 

- c. Descargar notas de estudiantes en una asignatura dictada. 

- d. Editar notas de asignaturas dictadas en el semestre actual. 

- - i. Editar notas mediante interacción con la aplicación. 

- - ii. Editar notas mediante un archivo de Excel. 

4. Administrativo 

- a. Acciones sobre estudiantes 

- - i. Ver semestres cursados por estudiante. 

- - ii. Ver asignaturas y notas en un periodo académico. 

- b. Acciones sobre profesores 

- - i. Ver periodos en los que un profesor dictó materias. 

- - ii. Ver asignaturas dictadas por un profesor en un periodo académico. 

- - iii. Ver estudiantes y notas de asignaturas dictadas en un periodo académico. 

- c. Acciones sobre asignaturas 

- - i. Ver periodos académicos donde se dictaron asignaturas. 

- - ii. Ver asignaturas dictadas en un periodo académico. 

- - iii. Ver profesores y grupos de una asignatura en un periodo académico. 

- - iv. Ver notas de estudiantes de un grupo de una asignatura dictada en un periodo académico. 

- - v. Editar porcentaje de calificaciones  

- d. Generar reportes 

- - i. Reporte de estudiante. 

- - ii. Reporte de asignatura en un determinado periodo. 

- e. Importar información 

- - i. Importar información de estudiantes en un periodo académico. 

- - ii. Importar información de asignaturas dictadas 

- - iii. Importar información de empleados. 

- f. Exportar información 

- g. Crear usuarios 

- h. Acciones sobre Alertas 

- - i. Ver y borrar alertas. 

- - ii. Generar alertas manuales 

# 0. Caso base

Cuando se inicia la aplicación el único usuario existente es el usuario admin cuya contraseña es admin. Ingresamos como se muestra en la imagen:

![admin_login](https://user-images.githubusercontent.com/33558020/87900253-72f6ee00-ca19-11ea-9c2e-ea6e80482c76.PNG)

Luego cambiamos la contraseña

![Alt text](https://user-images.githubusercontent.com/33558020/87893895-d3306480-ca06-11ea-8ba8-ddc138be3fbc.PNG)

Es necesario despues ir a la pestaña administración y cargar el archivo de profesores en información profesores.

Para cargar el archivo de estudiantes

![aaaa](https://user-images.githubusercontent.com/33558020/87900454-029c9c80-ca1a-11ea-9088-a93b3575e286.PNG)


luego cargamos el archivo de las materias


![adios](https://user-images.githubusercontent.com/33558020/87900456-03353300-ca1a-11ea-9905-e18b930ac5dc.PNG)

Si todo se hizo bien aparece:

![listo](https://user-images.githubusercontent.com/33558020/87900448-003a4280-ca1a-11ea-8304-8bdfa68c19f7.PNG)





# 1. Iniciando sesión:  

Para cualquier perfil, si es la primera vez que ingresa a la aplicación, al ser registrado por un administrador le deberá llegar un correo con un usuario y contraseña generados por la aplicación a su correo institucional. Con estos datos deberá ingresar e inmediatamente el sistema le solicitará cambiar su contraseña.  

![ingreso_app](https://user-images.githubusercontent.com/33558020/87897644-9b7aea00-ca11-11ea-8563-aaa90dadab54.PNG)

Cada vez que un usuario ingrese a la aplicación esta detectará que rol es el que desempeña, es decir, si es un estudiante, profesor, administrador o profesor/administrador. En el caso de ser un administrador y profesor la aplicación le permitirá elegir con cual perfil desea ingresar. 

![login](https://user-images.githubusercontent.com/33558020/87895657-94e97400-ca0b-11ea-82fd-3b36e025d5e8.PNG)

Automaticamente tendrá que modificar la contraseña.

![Alt text](https://user-images.githubusercontent.com/33558020/87893895-d3306480-ca06-11ea-8ba8-ddc138be3fbc.PNG)

Si el usuario ya existe el sistema le pide su correo para enviarle una contraseña nueva.

![usuario_ya](https://user-images.githubusercontent.com/33558020/87898060-ce71ad80-ca12-11ea-86fd-da2be4940f90.PNG)

En caso tal de que un usuario sea administrador y profesor el sistema le pide al usuario como ingresar:

![dilema](https://user-images.githubusercontent.com/33558020/87895647-931fb080-ca0b-11ea-92fe-d38e05657f6b.PNG)

# 2. Estudiante:
Una vez se haya iniciado sesión, la aplicación abrirá una ventana con las asignaturas y notas del último periodo académico registrado, donde además podrá acceder a todas las funcionalidades que tiene el estudiante dentro de Epsilon: 

Ventana inicial
![Alt text](https://user-images.githubusercontent.com/33558020/87893607-01fa0b00-ca06-11ea-9d92-02daad1e30cc.PNG)

**a. Datos personales:** Accediendo a la opción de “Datos personales” el estudiante podrá ver información tal como nombre, correo institucional, el código de estudiante, entre otros.

![Alt text](https://user-images.githubusercontent.com/33558020/87893896-d3c8fb00-ca06-11ea-8cde-54677e3e0c83.PNG)


**b. Ver notas de asignaturas de un periodo académico:**  Accediendo a la opción de datos académicos podrá elegir el periodo académico (matriculado) del cual desea obtener la información. Ya elegido el periodo la aplicación mostrará todas las asignaturas vistas en ese semestre junto con sus notas por cohorte.

![Alt text](https://user-images.githubusercontent.com/33558020/87893898-d4fa2800-ca06-11ea-8b4a-33abf65b4732.PNG)

Calificaciones por periodo

![Alt text](https://user-images.githubusercontent.com/33558020/87893902-d592be80-ca06-11ea-9be3-8789c4e5c884.PNG)


**c. Descargar notas de un periodo académico:** Cuando se esté consultando las notas de un periodo académico tendrá la posibilidad de descargar un archivo con esta información, este archivo será en formato CSV el cual podrá abrir con Excel. 

Botón de descarga

![boton_descarga](https://user-images.githubusercontent.com/33558020/87898704-8f445c00-ca14-11ea-908e-f935a5ddc09e.PNG)

Excel descargado:

![notas_excel](https://user-images.githubusercontent.com/33558020/87898713-966b6a00-ca14-11ea-9c93-bb94249f5e43.PNG)

**d. Ver y borrar alertas:**  En cualquier momento el estudiante podrá observar todas las alertas asociadas a su perfil accediendo por el icono de la campana, la cual indicará la cantidad de alertas no observadas hasta el momento. Habiendo ingresado a esta opción el estudiante tendrá información más detallada de cada alerta y tendrá la opción de borrarlas si así lo desea oprimiendo el botón de “Borrar”. 

Icono de alertas

![icono](https://user-images.githubusercontent.com/33558020/87898818-dcc0c900-ca14-11ea-827d-e5a951ba4bab.PNG)

Ventana de alertas

![Alt text](https://user-images.githubusercontent.com/33558020/87894106-6ff30200-ca07-11ea-811d-3c363f97c868.PNG)


# 3. Profesor

Una vez se haya iniciado sesión, la aplicación abrirá una ventana con las asignaturas que se encuentra dictando en el último periodo académico registrado: 

![main_profesor](https://user-images.githubusercontent.com/33558020/87894540-a54c1f80-ca08-11ea-950a-6f81788a9117.PNG)

**a. Ver materias dictadas de un periodo académico:** Ingresando a la opción de “Historial de materias”, el profesor podrá observar los periodos académicos en los que ha dictado por lo menos una asignatura. Seleccionando cualquiera de estos periodos se le mostrará una lista de asignaturas con el o los respectivos grupos que dictó. 

Menú periodos académicos donde el profesor dictó al menos una asignatura

![periodos](https://user-images.githubusercontent.com/33558020/87894546-a715e300-ca08-11ea-80aa-c830d01b63b8.PNG)

Menú asignaturas dictadas en el periodo 2020-2. 

![materias_periodos](https://user-images.githubusercontent.com/33558020/87894541-a5e4b600-ca08-11ea-9d8a-5f17caaef8c4.PNG)



**b. Ver estudiantes y notas de una asignatura dictada:** tras haber seleccionado una asignatura a partir del inciso anterior (a), va a aparecer una tabla con los estudiantes y sus respectivas notas en esta asignatura. 

Notas de estudiantes en la asignatura elegida

![notas_periodos](https://user-images.githubusercontent.com/33558020/87894545-a67d4c80-ca08-11ea-9e84-9597fec1f518.PNG)

**c. Descargar notas de estudiantes en una asignatura dictada:**  Tras haber seleccionado una asignatura a partir del inciso (a), se puede descargar la información sobre los estudiantes oprimiendo el botón “descargar”. Este archivo será en formato CSV el cual podrá abrir con Excel.  
Ejemplo botón Descargar. 

![descarga_notas](https://user-images.githubusercontent.com/33558020/87899163-eac31980-ca15-11ea-8662-cdf1722c7934.PNG)


**d. Editar notas de asignaturas dictadas en el semestre actual:** en la tabla de notas de estudiantes aparecen botones de editar y de subir las notas mediante un Excel, a continuación, explicamos estas dos funcionalidades. 

**i. Editar notas mediante interacción con la aplicación:**  en este punto hacemos referencia a la funcionalidad de editar las notas directamente en la tabla que se muestra en la aplicación, para usar esta función debemos dar clic en el botón editar, luego se habilitará la edición de las casillas que contienen notas en la tabla, para editar una casilla es suficiente con dar clic en esta e ingresar el valor deseado, tras haber ingresado los datos en cuestión se da clic en el botón de guardar. 

![edicion_notas](https://user-images.githubusercontent.com/33558020/87894547-a715e300-ca08-11ea-8baf-c8fda2e88c45.PNG)

**ii. Editar notas mediante un archivo de Excel:** para este apartado es posible hacer el cambio en las notas de los estudiantes de la asignatura elegida mediante un archivo de Excel que contenga esta información, cabe destacar que se debe tener un formato igual al que se mostrará a continuación. 

![archivo_Ex](https://user-images.githubusercontent.com/33558020/87899253-3fff2b00-ca16-11ea-90e4-b50785a2b7be.PNG)


# 4. Administrativo

Una vez se haya iniciado sesión, la aplicación abrirá una ventana vacía con las funcionalidades del administrador:

![main_Admin](https://user-images.githubusercontent.com/33558020/87895658-95820a80-ca0b-11ea-8b0d-49da3654b811.PNG)


**a. Acciones sobre estudiantes:** En el apartado estudiantes el administrador podrá ver todos los estudiantes registrados en la aplicación además de un pequeño resumen de estos, podrá generar reportes pulsando el botón al final de la información del estudiante. 

![lista_estudiantes](https://user-images.githubusercontent.com/33558020/87895651-93b84700-ca0b-11ea-81df-2cbc3aa63a6a.PNG)

**i. Ver semestres cursados por estudiante:**  Luego de seleccionar alguno de los estudiantes, el administrador podrá ver los periodos en los que ese estudiante registró alguna asignatura. 

![periodos_estu](https://user-images.githubusercontent.com/33558020/87895625-8dc26600-ca0b-11ea-8a1a-533e0c19efbb.PNG)

**ii. Ver asignaturas y notas en un periodo académico:** Si el administrador desea también puede descargar la información del desempeño del estudiante en alguno de estos periodos. 

![notas_periodos_estu](https://user-images.githubusercontent.com/33558020/87895665-974bce00-ca0b-11ea-93d3-797440673253.PNG)

**b. Acciones sobre profesores**

![lista_profesores](https://user-images.githubusercontent.com/33558020/87895652-9450dd80-ca0b-11ea-8cc2-3c3fab9d373c.PNG)

**i. Ver periodos en los que un profesor dictó materias:** Al ingresar a la opción de “Profesores” y seleccionar un profesor se desplegarán todos los distintos periodos académicos en los que este dicto al menos una asignatura. 

![periodos_profesor](https://user-images.githubusercontent.com/33558020/87895631-8ef39300-ca0b-11ea-85d9-e4748b6f1815.PNG)

**ii. Ver asignaturas dictadas por un profesor en un periodo académico:** Al seleccionar un periodo académico, como se describe en el inciso b-i, se desplegarán las asignaturas dictadas por el profesor en el periodo académico consultado. 

**iii. Ver estudiantes y notas de asignaturas dictadas en un periodo académico:** El administrador al elegir la asignatura dictada por el profesor en el periodo académico especifico, la información que se le mostrará es la del desempeño de los estudiantes en esta. 

![notas_periodos_profe](https://user-images.githubusercontent.com/33558020/87895666-97e46480-ca0b-11ea-9bb1-fe5d4a25d30c.PNG)


**c. Acciones sobre asignaturas:** 

**i. Ver periodos académicos donde se dictaron asignaturas:** Al seleccionar la opción de “Materias” se obtendrá un listado de todos los periodos académicos en los que se han dictado por lo menos una asignatura. 

![periodos_materias](https://user-images.githubusercontent.com/33558020/87895627-8e5afc80-ca0b-11ea-859f-67b2513e2d5d.PNG)


**ii. Ver asignaturas dictadas en un periodo académico:** Seleccionando un periodo académico (como se describe en el punto anterior), se obtendrá un listado de todas las asignaturas que fueron o son dictadas en el periodo seleccionado con sus respectivos códigos de asignatura y créditos. 

![listado_materias](https://user-images.githubusercontent.com/33558020/87895655-9450dd80-ca0b-11ea-9194-d5af2186a7b9.PNG)


**iii. Ver profesores y grupos de una asignatura en un periodo académico:** Seleccionando una asignatura en un periodo académico determinado (como se describe en los puntos anteriores) se obtendrá un listado de los grupos existentes en el periodo determinado y los respectivos profesores que dictaron la materia. 

![grupos](https://user-images.githubusercontent.com/33558020/87895649-931fb080-ca0b-11ea-9e7f-0c1703a43902.PNG)

**iv. Ver notas de estudiantes de un grupo de una asignatura dictada en un periodo académico:** El administrador podrá consultar una asignatura y de esta un grupo respectivo donde podrá ver las respectivas notas de los estudiantes en los 5 cortes del periodo. 

![notas_grupo](https://user-images.githubusercontent.com/33558020/87895662-96b33780-ca0b-11ea-8618-a0a6a2938a2a.PNG)


**v. Editar porcentaje de calificaciones:** Al ingresar a la opción de “Materias” y oprimir el botón de “Editar”, se pueden cambiar los créditos y los porcentajes de relevancia de las notas en cada materia. Esta acción solo afecta al último periodo registrado. Para guardar los cambios ingresados se oprime “Guardar” y las modificaciones se efectuarán de manera automática.   

![bb](https://user-images.githubusercontent.com/33558020/87899637-6e313a80-ca17-11ea-8d9a-298853e4dec0.PNG)


**d. Generar reportes:**

**i. Reporte de estudiante:** Al ingresar en la opción de “Estudiantes” se puede generar un reporte de los promedios por periodo académico al oprimir el botón en el extremo derecho de cada estudiante registrado. Este reporte se desplegará en la pantalla principal y posee la opción de descargarlo. 

![reporte_estudiante](https://user-images.githubusercontent.com/33558020/87895633-8f8c2980-ca0b-11ea-9630-9c3234fdf4b8.PNG)


**ii. Reporte de asignatura en un determinado periodo:** Al ingresar a la opción de “Materias” y seleccionar un determinado periodo, el usuario podrá generar un reporte con el botón en el extremo derecho de cada asignatura. Este reporte se desplegará en la pantalla principal y posee la opción de descargarlo. 

![reporte_grupos](https://user-images.githubusercontent.com/33558020/87895636-9024c000-ca0b-11ea-89a3-7f91158c1f1d.PNG)


**e. Importar documentos:** El rol de administrador tiene la capacidad de poder ingresar la información sobre los estudiantes, profesores y cursos que habrá en un periodo académico, al dirigirse a la ventana “Administración” aparecerán las siguientes opciones: 


![administracion](https://user-images.githubusercontent.com/33558020/87895639-90bd5680-ca0b-11ea-83a0-3939637626b1.PNG)


**i. Importar información de estudiantes en un periodo académico:*** En este apartado el administrador mediante un archivo de Excel con un formato especifico puede ingresar la información de los distintos estudiantes que haya, tanto inscritos previamente como nuevos. Por defecto a los nuevos estudiantes se les hará el proceso comentado en el apartado de Iniciando sesión, por otro lado, este archivo tiene las clases y demás información pertinente con referencia en la matrícula de los estudiantes. 

![bb](https://user-images.githubusercontent.com/33558020/87899851-2959d380-ca18-11ea-898b-caada3dd573b.PNG)

**ii. Importar información de asignaturas dictadas:** A partir del proceso realizado en el apartado anterior la plataforma nos habilitará la opción de manera inmediata para poder ingresar la información de los profesores con las asignaturas que estos dictarán, para esto también se tiene un formato que se mostrará a continuación. 

![cc](https://user-images.githubusercontent.com/33558020/87899852-29f26a00-ca18-11ea-8459-d0ec39c238ad.PNG)

**iii. Importar información de empleados:** Se podrá importar la información de los empleados que se encuentre en un documento de Excel, donde se tenga la información personal del empleado y el o los roles que este empleará (administrador, profesor o ambos), el formato para esto es el siguiente: 

![dd](https://user-images.githubusercontent.com/33558020/87899853-2a8b0080-ca18-11ea-9844-9244fb8bc175.PNG)

**f. Exportar información:**  

**i. Asignaturas y notas de un estudiante en el último semestre:** Al ingresar a la opción de “Estudiantes” y seleccionar un estudiante, el administrador ingresara a una ventana con las asignaturas y notas del último semestre registrado. Al oprimir el botón de “descargar”, se descargará un archivo .csv con las asignaturas y notas del estudiante. 

![1](https://user-images.githubusercontent.com/33558020/87900792-fb29c300-ca1a-11ea-9862-02896a25f41f.PNG)

**ii. Reporte de promedios por semestre cursado:** Al ingresar a la opción de “Estudiante” el usuario podrá oprimir en la casilla del extremo derecho de cada estudiante para obtener un reporte del promedio del estudiante por semestre cursado. Al oprimir sobre “descargar” obtendrá una imagen del gráfico.

![2](https://user-images.githubusercontent.com/33558020/87900794-fbc25980-ca1a-11ea-8907-00993a53e9da.PNG)

**iii. Estudiantes y notas de una materia y grupo específico:**  ingresar a “Materias”, y seleccionar un periodo específico, el administrador podrá escoger una asignatura dictada durante ese semestre, en donde podrá descargar un archivo .CSV con los estudiantes y notas al oprimir sobre ‘descarga’.    
udiantes y notas de una materia y grupo específico: Al ingresar a “Materias”, y seleccionar un periodo específico, el administrador podrá escoger una asignatura dictada durante ese semestre, en donde podrá descargar un archivo .CSV con los estudiantes y notas al oprimir sobre ‘descarga’.  

**iv. Reporte de promedios de una materia** Al ingresar la opción de “Materias”, selecciona una materia, el administrador ingresara a una ventana con las asignaturas, si hace clic en la imagen de gráficas, podrá visualizar un reporte tipo histograma donde se podrá consultar el rango de notas obtenidas por los estudiantes en intervalos de 0.5, es decir; (0,0.5](0.5,1]…(4.5,5].

![4](https://user-images.githubusercontent.com/33558020/87900795-fbc25980-ca1a-11ea-90be-285763a82db2.PNG)


**g. Crear usuario:** Si desea crear un nuevo usuario debe dirigirse a la ventana administración y en esta seleccionar la opción “Crear usuario nuevo”, ahí tendrá la posibilidad de elegir el rol correspondiente para este nuevo registro y seleccionar el archivo CSV del cual se obtendrá esta información. 

![crear_usuario](https://user-images.githubusercontent.com/33558020/87899998-9a00f000-ca18-11ea-9d8b-0905ddcf7fd2.PNG)

**h. Acciones sobre alertas **

**i. Ver y borrar alertas:** Cuando se genere una alerta de las diferentes posibilidades, a el administrador en el signo de la campana le llegara una notificación de alerta. Donde podrá consultar todas las alertas recibidas y si es del gusto del administrador, podrá eliminar cada alerta de manera individual. 

![alertas](https://user-images.githubusercontent.com/33558020/87895642-91ee8380-ca0b-11ea-9ec5-ba03a2cb9508.PNG)

**ii. Generar alertas manuales:** El administrador, podrá genera una alerta manual dependiendo del tipo de alerta. Además, podrá ingresar un texto como descripción del caso generado. 

![alerta_manual](https://user-images.githubusercontent.com/33558020/87895640-9155ed00-ca0b-11ea-97e9-7271361d766d.PNG)

**iii. Tipos de alertas:** 

**i. Nota baja:** El estudiante recibió una nota de 2 a 3 en algún corte. 

**ii. Nota muy baja:** El estudiante recibió una nota de entre 0 y 2 en algún corte. 

**iii. Posible pérdida de materia:** Esta alerta funciona en base a que dado las notas ya sea de primer o segundo corte, un modelo de predicción destinado para la materia predice si el estudiante se encuentra en riesgo de pérdida. 



