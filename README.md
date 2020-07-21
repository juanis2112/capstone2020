# Epsilon: Instalación y Configuración 

**NOTA**
Los siguientes pasos debe ejecutarlos desde su entorno local o desde la instancia en la cual va a configurar su servidor.

## Clonando el Repositorio

```bash
$ git clone https://github.com/juanis2112/capstone2020
```

## Accediendo al release

Primero debe acceder a la carpeta de su repositorio ejecutando:

```bash
$ cd capstone
```

Para acceder a la rama con el release final de la aplicación debe ejecutar:

```bash
$ git checkout final
```

## Creando un ambiente 

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

### Generando la base de datos

Para generar la base de datos de la aplicación es necesario contar con PostgreSQL y pgAdmin4 y generar una base de datos con nombre `capstone` desde pgAdmin4 o la terminal. 

Para que la conexión con su base de datos sea exitosa, debe abrir el archivo `Epsilon/App.py` de su repositorio y reemplazar los strings que corresponden "user" y "password", por su usuario y contraseña correspondientes a su base de datos.

## Trabajando desde su entorno local 

### Corriendo Epsilon

Para ejecutar la aplicación, debe ubicarse en la carpeta Epsilon:

```bash
$ cd Epsilon
```

Primero, es necesario correr el archivo `ML.py` para actualizar los modelos de machine learning:

```bash
$ python ML.py
```

Ahora debe correr la aplicación desde el repositorio:

```bash
$ python App.py
```

Si su ejercución fue exitosa, aparecerá el siguiente mensaje en la terminal
`Running on http://127.0.0.1:2000/`

Ahora debe copiar esta dirección en su porta papeles y péguelo en cualquier navegador para abrir la aplicación.

## Trabajando desde un Servidor

### Creación de la instancia en EC2

Debe ingresar a la página de [AWS](https://aws.amazon.com/es/) con su cuenta. Estando en la consola de AWS, debe buscar el servicio de EC2 en donde encontrará a  mano izquierda la opción `instancias`, la cuál lo llevara a la consola de instancias que tenemos en el momento. Para su nuestra instancia debe presionar el botón `Launch Instance`.

A continuación debe elegir las caracteristicas de su instancia, las cuales deberían cumplir con los requerimientos necesarios para alojar su aplicación. Como recomnedanción puede considerar las siguientes caracteristicas:

1. *Choose an Amazon Machine Image*: Ubuntu server 18.04 LTS
2. *Choose an Instance Type*: t2.micro (Free tier eligible)
3. *Configure Instance Details*: Dejar configuración por defecto.
4. *Add Storage*: Configurar el tamaño de la instancia a 8 GIB.
5. *Add Tags*: Dejar configuración por defecto.
6. *Configure Security Group*: Configurar el puerto SSH para su instancia.
7. *Review*: Revisar las caracteristicas que se han seleccionado anteriormente para luego lanzar la instancia.

Una vez que se halla creado su instancia debe proceder a configurar su llave de acceso, la cual será un archivo con extensión `.pem`. Dependiendo del sistema operativo que se encuentre utilizando, la conexión con la instancia se realiza de manera diferente. Si se utiliza  Windows deberá utilizar la herramienta [putty](https://docs.aws.amazon.com/es_es/AWSEC2/latest/UserGuide/putty.html) para conectarse a la instancia. Por otro lado, si utiliza una distribución de linux deberá ejecutar el siguiente comando en la terminal:

```bash
$ ssh -i "PATH del archivo.pem" ubuntu@"Public DNS (IPv4)"
```

**NOTA**
Antes de ejecutar el comando anterior debe asegurarse que su archivo cuente con los permisos correspondientes. Para ello ejecute el comando:

```bash
$ chmod 400 "PATH/DEL/ARCHIVO.pem"
```

Cabe resaltar que el `Public DNS (IPv4)` es una dirección única y en la cual la podrá encontrar en las características de la instancia creada.


### Configuración de la IP elástica

Para tener acceso a su instancia por medio de una dirección IP debe crear una IP pública. En la consola de EC2 debe dirigirse a mano izquierda a la opción `Direcciones IP elástica`, en donde encontrará el botón `Asignar ip elástica`.  Despúes debe seleccionar `Grupo de direcciones IPv4 de Amazon` y posteriormente `asignar`. Para finalizar el emparejamiento con la IP elástica y nuestra instancia, debe seleccionar en la casilla de acciones la opción de `asociar la dirección ip elástica`, en donde debe seleccionar su instancia ya creada.


### Instalación de nginx

El servidor web a utilizar sera nginx, el cual se puede instalar con el siguiente comando

```bash
$ sudo apt update
$ sudo apt install nginx
```

Para la configuración del servidor web debe ingresar a la siguiente carpeta y crear un archivo llamado `Epsilon`:

```bash
$ cd /etc/nginx/sites-enabled/
$ sudo vim Epsilon
```

A continuación debe colocar la siguiente configuración a este archivo
```bash
server {
	listen 80 default_server;
	server_name Ip elástica de la instancia;
	location /{
	proxy_pass http://127.0.0.1:8000;
    }
}
```

Ahora debe proceder a la instalación de gunicron3 el cual le permitirá realizar la conexión entre el servidor instalado anteriormente y la instancia de AWS. Debe ejecutar el siguiente comando

```bash
$ sudo apt update
$ sudo apt install gunicorn3
```
### Corriendo Epsilon

Teniendo su archivo de la aplicación ya configurado podrá realizar la activación del servidor y la ejecución del programa con los siguientes comandos

```bash
$ sudo systemctl start nginx
$ cd Epsilon
$ gunicorn3 ML:app
$ gunicorn3 App:app
```
La ejecución del gunicorn 3 debe realizarse en la carpeta en donde se encuentra el archivo de flask.

**NOTA**
La aplicación ya se encuentra corriendo en una instancia con la siguiente dirección:
http://54.225.233.22/

