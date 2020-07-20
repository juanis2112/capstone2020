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




![main_profesor](https://user-images.githubusercontent.com/33558020/87894540-a54c1f80-ca08-11ea-950a-6f81788a9117.PNG)
![materias_periodos](https://user-images.githubusercontent.com/33558020/87894541-a5e4b600-ca08-11ea-9d8a-5f17caaef8c4.PNG)
![notas](https://user-images.githubusercontent.com/33558020/87894543-a5e4b600-ca08-11ea-995a-61cf5723409a.PNG)
![notas_periodos](https://user-images.githubusercontent.com/33558020/87894545-a67d4c80-ca08-11ea-9e84-9597fec1f518.PNG)
![periodos](https://user-images.githubusercontent.com/33558020/87894546-a715e300-ca08-11ea-80aa-c830d01b63b8.PNG)
![edicion_notas](https://user-images.githubusercontent.com/33558020/87894547-a715e300-ca08-11ea-8baf-c8fda2e88c45.PNG)
![login](https://user-images.githubusercontent.com/33558020/87894549-a7ae7980-ca08-11ea-95d5-a169bca15892.PNG)







