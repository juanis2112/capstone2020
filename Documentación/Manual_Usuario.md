
# Manuel de Usuario


# Índice

1.Iniciando sesión. 

2.Estudiante 

- Ver datos personales. 

- Ver notas de asignaturas de un periodo académico.  

- Descargar notas de un periodo académico. 

- Ver y borrar alertas 

3. Profesor 

- Ver materias dictadas de un periodo académico. 

- Ver estudiantes y notas de una asignatura dictada. 

- Descargar notas de estudiantes en una asignatura dictada. 

- Editar notas de asignaturas dictadas en el semestre actual. 

- - Editar notas mediante interacción con la aplicación. 

- - Editar notas mediante un archivo de Excel. 

4. Administrativo 

- Acciones sobre estudiantes 

- - Ver semestres cursados por estudiante. 

- - Ver asignaturas y notas en un periodo académico. 

- Acciones sobre profesores 

- - Ver periodos en los que un profesor dictó materias. 

- - Ver asignaturas dictadas por un profesor en un periodo académico. 

- - Ver estudiantes y notas de asignaturas dictadas en un periodo académico. 

- Acciones sobre asignaturas 

- - Ver periodos académicos donde se dictaron asignaturas. 

- - Ver asignaturas dictadas en un periodo académico. 

- - Ver profesores y grupos de una asignatura en un periodo académico. 

- - Ver notas de estudiantes de un grupo de una asignatura dictada en un periodo académico. 

- - Editar porcentaje de calificaciones  

- Generar reportes 

- - Reporte de estudiante. 

- - Reporte de asignatura en un determinado periodo. 

- Importar información 

- - Importar información de estudiantes en un periodo académico. 

- - Importar información de asignaturas dictadas 

- - Importar información de empleados. 

- Exportar información 

- Crear usuarios 

- Acciones sobre Alertas 

- - Ver y borrar alertas. 

- - Generar alertas manuales 

- Todo lo respecto a los modelos de machine laearning 

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

Se puede generar un reporte por periodo

![reporte_periodo_profe](https://user-images.githubusercontent.com/33558020/87895637-9024c000-ca0b-11ea-84e1-093305fc7521.PNG)








