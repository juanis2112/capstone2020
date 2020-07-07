# Capstone 2020-I: Epsilon 
## Instalación y Configuración

### Clonando el Repositorio

```bash
$ git clone https://github.com/juanis2112/capstone2020
```

### Accediendo al release

Primero debe acceder a la carpeta de su repositorio ejecutando:

```bash
$ cd capstone
```

Para acceder a la rama con el release 0.1 de la aplicación debe ejecutar:

```bash
$ git checkout v0.1
```

### Generando la base de datos

Para generar la base de datos de la aplicación es necesario contar con PostgreSQL y pgAdmin4 y generar una base de datos con nombre `capstone` desde pgAdmin4 o la terminal. 

Primero debe correr el archivo `creacion_bd.sql` en el `Query Tool` de su base de datos `capstone`. Luego, debe abrir el archivo `insercion_datos.sql` con un editor de texto y en las lineas 54, 55 y 56 en el path, agregué el path donde se encuentra su carpeta capstone donde esta su repositorio antes de `/capstone` y guarde los cambios.

Una vez los paths correspondan con los archivos en su repositorio, debe correr el archivo `insercion_datos.sql` en el `Query Tool` de su base de datos `capstone`.

Finalmente, para que la conexión con su base de datos sea exitosa, debe abrir el archivo `Epsilon/App.py de su repositorio y reemplazar los strings que corresponden "user" y "password" en la linea 18, por su usuario y contraseña correspondientes a su base de datos.

### Creando un ambiente 

Para organizar las librerias necesarias de Python, debe crear un ambiente de conda con python.

```bash
$ conda create -n capstone python=3.7
$ conda activate capstone
```

Para Linux puede usar `virtualenv` en vez de Conda.

```bash
$ mkvirtualenv capstone
$ workon capstone
```

### Instalando las dependencias


Después de crear el ambiente, debe instalar las dependecias, las cuales se encuentran todas en el archivo de requirements.txt

```bash
$ conda install --file requirements.txt
```

Si esta usando `pip` y `virtualenv` corra:

```bash
$ pip install -r requirements.txt 
```

### Corriendo Epsilon

Para correr la aplicación desde el repositorio:

```bash
$ python Epsilon/App.py
```
Si su ejercución fue exitosa, aparecerá el siguiente mensaje en la terminal
`Running on http://127.0.0.1:2000/`

Ahora debe copiar esta dirección en su porta papeles y péguelo en cualquier navegador para abrir la aplicación.




