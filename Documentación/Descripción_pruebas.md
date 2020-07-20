# Descripción pruebas


En este texto abordaremos los diferentes tipos de pruebas funcionales con el fin de que la aplicación se ejecute de manera apropiado. 

 

**Unitarias:**  En este tipo de prueba se verifican los componentes individuales de un programa que funcione aisladamente, como deben de comportarse, cuando deben hallar un error y cuando deben cumplir su cometido. Este tipo de pruebas de bajo nivel ponen a prueba diferentes métodos, clases, funciones y módulos. (¡Este tipo de prueba debe estar en código!) 

**Resultado pruebas:** Este tipo de prueba ha sido aplicado constantemente durante el desarrollo del producto, desde el desarrollo de Front end, Backend, Bases de datos y generación de modelos. Donde en cada función le paso como argumentos los casos que esperamos que en promedio ocurran tanto como los casos límites.  No pudimos lograr hacer las pruebas formales un un archivo de test. 

**Integración:** Este tipo de pruebas verifica que los módulos o servicios de la aplicación interactúan correctamente. Este orden de la integración de los componentes se basa principalmente en la arquitectura. 

**Resultado pruebas:** Al realizar las pruebas unitarias, una vez se dio el visto bueno. Se procedió a realizar las pruebas de integración que se encarga de mesclar este tipo de funciones tal que pudiera imitar un comportamiento del usuario. 

**Funcional:** Este tipo de prueba verifica que la aplicación cumple con los requerimientos de negocio. Se concentran en el resultado de las acciones que realiza el usuario. 

**Resultados:** De esta manera los requerimientos que debe cumplir la aplicación deben ser: 
- Seguimiento de estudiantes, incluyendo su desempeño académico. ✓ 
- Importación de notas en Excel.  ✓ 
- Reporte de notas directamente por parte de los profesores. ✓ 
- Sistema de Alertas. ✓ 
- Información almacenada de forma segura. ✓ 
- Garantía de que los usuarios puedan acceder a la aplicación. ✓ 
- Garantía que la aplicación no pueda ser utilizada por terceros sin autorización. ✓ 

# Pruebas de extremos: 
Son las pruebas que se hacen de principio a fin y que validan toda la experiencia que debe tener un usuario de la aplicación. 

**Resultado pruebas:**
# Estudiante

Simulamos la aplicación con el usuario Juanita Gómez.
![Alt text](https://user-images.githubusercontent.com/33558020/87893607-01fa0b00-ca06-11ea-9d92-02daad1e30cc.PNG)

En efecto el sistema nos pide cambio de contraseña para el usuario.
![Alt text](https://user-images.githubusercontent.com/33558020/87893895-d3306480-ca06-11ea-8ba8-ddc138be3fbc.PNG)

Podemos ingresar de manera correcta a la ventana principal del estudiante.
![Alt text](https://user-images.githubusercontent.com/33558020/87893900-d592be80-ca06-11ea-83b2-278dce0e311a.PNG)

Se puede ver correctamente los datos personales de Juanita y tambien la descarga de las notas se esta haciendo bien.
![Alt text](https://user-images.githubusercontent.com/33558020/87893896-d3c8fb00-ca06-11ea-8cde-54677e3e0c83.PNG)

Se puede ver el historico de periodos que ha visto la estudiante.
![Alt text](https://user-images.githubusercontent.com/33558020/87893898-d4fa2800-ca06-11ea-8b4a-33abf65b4732.PNG)

Y las materias vistas en cada periodo
![Alt text](https://user-images.githubusercontent.com/33558020/87893902-d592be80-ca06-11ea-9be3-8789c4e5c884.PNG)

Asimismo las alertas que tiene.
![Alt text](https://user-images.githubusercontent.com/33558020/87894106-6ff30200-ca07-11ea-811d-3c363f97c868.PNG)


# Profesor

Se hacen las pruebas con el usuario Germán Obando.

Login correcto.
![login](https://user-images.githubusercontent.com/33558020/87894549-a7ae7980-ca08-11ea-95d5-a169bca15892.PNG)

Cambio de contraseñan funciona.
![Alt text](https://user-images.githubusercontent.com/33558020/87893895-d3306480-ca06-11ea-8ba8-ddc138be3fbc.PNG)

Ventana principal del profesor.
![main_profesor](https://user-images.githubusercontent.com/33558020/87894540-a54c1f80-ca08-11ea-950a-6f81788a9117.PNG)

Puede visualizar correctamente las notas del periodo actual y descarga de notas y subida de acrhivos funciona bien.
![notas](https://user-images.githubusercontent.com/33558020/87894543-a5e4b600-ca08-11ea-995a-61cf5723409a.PNG)

Ve los periodos que ha dictado.
![periodos](https://user-images.githubusercontent.com/33558020/87894546-a715e300-ca08-11ea-80aa-c830d01b63b8.PNG)

Las materias tambien.
![materias_periodos](https://user-images.githubusercontent.com/33558020/87894541-a5e4b600-ca08-11ea-9d8a-5f17caaef8c4.PNG)

Sus respectivas notas.
![notas_periodos](https://user-images.githubusercontent.com/33558020/87894545-a67d4c80-ca08-11ea-9e84-9597fec1f518.PNG)

La edicion de notas de las materias del periodo actual funciona correctamente.
![edicion_notas](https://user-images.githubusercontent.com/33558020/87894547-a715e300-ca08-11ea-8baf-c8fda2e88c45.PNG)


# Administrador:

Se hacen las pruebas con el usuario Juan Perez
![login](https://user-images.githubusercontent.com/33558020/87895657-94e97400-ca0b-11ea-82fd-3b36e025d5e8.PNG)

Se cambia la contraseña correctamente.
![Alt text](https://user-images.githubusercontent.com/33558020/87893895-d3306480-ca06-11ea-8ba8-ddc138be3fbc.PNG)

En caso de ser profesor o administrador puede decidir por cual acceder.
![dilema](https://user-images.githubusercontent.com/33558020/87895647-931fb080-ca0b-11ea-92fe-d38e05657f6b.PNG)

Venta principal del administrador.
![main_Admin](https://user-images.githubusercontent.com/33558020/87895658-95820a80-ca0b-11ea-8b0d-49da3654b811.PNG)

Puede ver a todos los estudiantes y el buscador funciona correctamente
![lista_estudiantes](https://user-images.githubusercontent.com/33558020/87895651-93b84700-ca0b-11ea-81df-2cbc3aa63a6a.PNG)

Puede ver el progreso de los estudiantes
![reporte_estudiante](https://user-images.githubusercontent.com/33558020/87895633-8f8c2980-ca0b-11ea-9630-9c3234fdf4b8.PNG)

Asimismo ingresar a su información personal, notas por periodo, e historial academico.
![notas_estu](https://user-images.githubusercontent.com/33558020/87895661-961aa100-ca0b-11ea-9caf-660d2824cb66.PNG)
![periodos_estu](https://user-images.githubusercontent.com/33558020/87895625-8dc26600-ca0b-11ea-8a1a-533e0c19efbb.PNG)
![notas_periodos_estu](https://user-images.githubusercontent.com/33558020/87895665-974bce00-ca0b-11ea-93d3-797440673253.PNG)
![datos_estu](https://user-images.githubusercontent.com/33558020/87895644-92871a00-ca0b-11ea-898d-6387b5f919ec.PNG)

Tambien ve el listado de los profesores, las materias dictadas por periodo y su correspondiente nota
![lista_profesores](https://user-images.githubusercontent.com/33558020/87895652-9450dd80-ca0b-11ea-8cc2-3c3fab9d373c.PNG)
![periodos_profesor](https://user-images.githubusercontent.com/33558020/87895631-8ef39300-ca0b-11ea-85d9-e4748b6f1815.PNG)
![notas_periodos_profe](https://user-images.githubusercontent.com/33558020/87895666-97e46480-ca0b-11ea-9bb1-fe5d4a25d30c.PNG)
![reporte_periodo_profe](https://user-images.githubusercontent.com/33558020/87895637-9024c000-ca0b-11ea-84e1-093305fc7521.PNG)


Por parte de las materias, ve por periodo cada materia
![periodos_materias](https://user-images.githubusercontent.com/33558020/87895627-8e5afc80-ca0b-11ea-859f-67b2513e2d5d.PNG)
![listado_materias](https://user-images.githubusercontent.com/33558020/87895655-9450dd80-ca0b-11ea-9194-d5af2186a7b9.PNG)

Por materia puede ver un reporte comparativo de los grupos de la misma
![reporte_grupos](https://user-images.githubusercontent.com/33558020/87895636-9024c000-ca0b-11ea-89a3-7f91158c1f1d.PNG)

Puede ver las notas por grupo
![grupos](https://user-images.githubusercontent.com/33558020/87895649-931fb080-ca0b-11ea-9e7f-0c1703a43902.PNG)
![notas_grupo](https://user-images.githubusercontent.com/33558020/87895662-96b33780-ca0b-11ea-8618-a0a6a2938a2a.PNG)

En administración puede cargar correctamente los archivos de profesores, estudiantes, y materias por periodo.
![administracion](https://user-images.githubusercontent.com/33558020/87895639-90bd5680-ca0b-11ea-83a0-3939637626b1.PNG)


Puede ver las alertas generadas a los estudiantes y puede crear alertas personalizadas.
![alerta_manual](https://user-images.githubusercontent.com/33558020/87895640-9155ed00-ca0b-11ea-97e9-7271361d766d.PNG)
![alertas](https://user-images.githubusercontent.com/33558020/87895642-91ee8380-ca0b-11ea-9ec5-ba03a2cb9508.PNG)



![materias_periodos](https://user-images.
githubusercontent.com/33558020/87895659-95820a80-ca0b-11ea-8809-76ec77804969.PNG)



#Pruebas de aceptación:
**A** continuación, hay un listado con las características aprobadas por el cliente:
•	Características visuales:
a.	Se eligió una paleta de colores adecuada (azul y colores claros de fondo) para la aplicación
b.	Diseño de la ventana de inicia sesión
c.	Se aprobaron las siguientes características para cada uno de los usuarios:
Para estudiantes:
-	Botón de Datos personales: para ver información del estudiante como nombres, apellidos, correo, número de documento y otra información. También se encuentra un botón para descargar la información personal
-	Botón de Datos académicos: para seleccionar el periodo académico que el estudiante desee y ver sus notas en cada una de las materias y cortes.
-	Notificación de alertas: botón de alertas para notificar al estudiante cuando tenga una nota baja.
Para profesores:
-	Botón Mis materias: para ver las materias que el profesor está dictando en el semestre actual. Al seleccionar una de las materias se puede ver las notas de los estudiantes en la materia, así como botones para editar, o descargar las notas actualmente registradas y botones para seleccionar un archivo y subir notas de la materia.
-	Botón Historial de materias:  para ver las notas que el profesor ha dictado anteriormente. Al seleccionar una de estas materias se puede ver las notas de primero a quinto corte y nota final de los estudiantes que la cursaron. 
Para administradores:
-	Botón de estudiantes: para ver todos los estudiantes inscritos en el último semestre. Para cada uno de ellos se puede ver el número de créditos inscritos y el promedio de cada uno. También se encuentra una barra de búsqueda para encontrar estudiantes por su nombre.
-	Botón de profesores: para acceder a información de cada uno de los profesores. Al seleccionar un profesor se puede ver los cursos que dicta, en qué periodo y las notas de los estudiantes en ese curso. También se encuentra una barra de búsqueda para encontrar profesores por su nombre
-	Botón de materias: para acceder a un semestre específico y ver las materias dictadas en ese semestre.
-	Botón de administración: para ver las opciones “Importar profesores”, “Importar información periodo académico” y “Crear usuario nuevo”. Al seleccionar cualquiera de estas opciones aparece una ventana con botones para cargar la información requerida.
-	Botones de gráficas: se puede ver una gráfica de notas por estudiante, de las notas en las materias por semestre o por profesor que las dicta.
-	Notificación y creación de alertas: ventana donde se puede ver las alertas que haya levantado el sistema sobre estudiantes en riesgo junto con botón para agregar alertas personalizadas. 


•	Características funcionales:
a.	Acceso web a la aplicación con su IP respectivo

b.	Alertas automáticas: Se validó que los modelos corrieran con los datos de entrenamiento subministrado por los clientes. De igual manera se revisó que los modelos se vuelvan a entrenar con la información de los datos y que se hicieran las respectivas predicciones de los riesgos de los diferentes tipos de materias y estudiantes.
Por otra parte, se revisó que se produjeran las alertas si un estudiante le fue mal en un corte, o en promedio a todos los estudiantes en una materia.
c.	Para estudiantes:
-	Consultas de los estudiantes sobre sus resultados académicos e información personal
d.	Para profesores:
-	Se notifica al profesor en caso de ingresar notas incorrectamente (mayores a 5, menores a 1 o ingresar caracteres no numéricos)
-	Importar archivo .csv con las notas de los estudiantes
-	Cambiar porcentajes de las materias como prefiera el profesor y verificar que la suma de los porcentajes sea correcta.
-	Consultar, modificar, cargar y descargar notas de estudiantes en cada una de las materias que dicta el profesor en el semestre actual. Además, también se puede ver gráficas de resultados de los estudiantes.
-	Consulta de notas del semestre pasado
e.	Para administradores:
-	Generar alertas manuales para enviarlas a los estudiantes
-	Consultas para ver notas por estudiante, profesor o curso
-	Importar información de profesores, de notas de un periodo académico y creación de nuevos usuarios a partir de archivos .csv
•	Características no funcionales: 
a.	Seguridad: las contraseñas están encriptadas en la base de datos
b.	Logging: tabla con registro de las acciones de los usuarios con la aplicación. Cada acción está clasificada en una de 3 categorías posibles dependiendo de su importancia 
c.	Verificación de roles (estudiante, profesor, administrador) para no acceder pasar de un rol a otro
d.	Conexión a la base de datos con una llave segura
