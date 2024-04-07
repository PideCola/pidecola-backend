# Pidecola Backend
Servicio backend de pidecolausb

## Setup Local
### Creacion de virtualenv
```
$ python -m venv <nombre del virtual env>
```

### Activacion del virtualenv
En Windows:
```
> <carpeta del virtualenv>\Scripts\activate
```

En Linux:
```
$ source /<carpeta del virtualenv>/bin/activate
```

### Instalacion de dependencias

Estando en el directorio del backend con el virtualenv activo

```
$ pip install -r requirements.txt
```

### Migracion de la base de datos

Esto es necesario siempre que se modifique algun archivo de modelos
y se debe hacer antes de activar el servidor por primera vez

```
$ python manage.py makemigrations
$ python manage.py migrate
```

### Activacion del servidor

Estando en el directorio del backend con el virtualenv activo

```
$ python manage.py runserver
```

### Creacion de usuario de admin
```
$ python manage.py createsuperuser
```
### Configuracion inicial

En Windows:
```
Get-Content setup.py | python manage.py shell
```

En Unix:
```
python manage.py shell < setup.py
```

## Setup con docker

Estando en el directorio del repo, construye la imagen con:
```bash
$ docker compose build
```
Espera a que termine, puede durar, depende de la conexión a internet

Luego, inicia el servicio con:
```bash
$ docker compose up
```

Si es la primera vez que ejecutas el servicio, debes realizar el proceso de setup inicial. No te preocupes por las migraciones, el comando ```docker compose up``` se encarga de aplicarlas al iniciar el servicio

## Setup inicial
### Poblar la base de datos

Crea los grupos/permisos y rutas por defecto:

``` bash
$ python manage.py shell < setup.py
```
No ejecutes este script mas de una vez

### Creación de superuser
Para utilizar el panel de administrador de django, debes crear un superusuario

``` bash
$ python manage.py createsuperuser
```
Esto te llevará por un proceso interactivo para asignar nombre de usuario y contraseña. Comprueba el estado del servicio iniciando sesion en el panel de administrador. Este se encuentra en: ```{BASE_URL}/api/v1/admin/``` donde BASE_URL es el dominio donde esta montado el servicio. Si lo estas ejecutando es la misma máquina, este debería ser ```http://localhost:8000/api/v1/admin/ ```

Terminado este proceso, ya puedes iniciar el servicio de frontend


### Entorno de desarrollo en docker

Vea que el archivo `compose.yaml` inicia el contenedor con un volumen. Esto sincroniza los archivos de la máquina anfitriona con el contenedor. Por tanto, los cambios en el código se verán reflejados en el contenedor.

Ahora, para ejecutar comandos en el contenedor, asegúrate que este está corriendo.

Ejecuta el siguiente comando:
```bash
$ docker ps
```
te retornará una tabla como esta, donde sólo importa el "Container id"
```
CONTAINER ID   IMAGE                  COMMAND                  CREATED        ...
53dbe6c8ab6b   pidecola_back-server   "sh -c 'python manag…"   5 minutes ago  ...
```
**IMPORTANTE**: El "container id" que te retornará será distinto.

Toma el container id que aparezca para "pidecola_back-server" y ejecuta el siguiente comando:

```bash
$ docker exec -it 53dbe6c8ab6b bash
```
Con esto estarás conectado al contenedor y puedes ejecutar comandos de bash. (¡Prueba con `ls -l`!)

Con esto ya puedes ejecutar los comandos de setup inicial indicados previamente.

#### Lidiando con migraciones en docker
Al hacer cambios en los modelos, debes ejecutar las migraciones.
Por sencillez, basta con que detengas el contenedor de docker y lo
vuelvas a ejecutar para aplicar el cambio.

En la terminal donde ejecutaste `docker compose up` puedes pulsar `CTRL+C` para detener el servicio.
Luego, vuelve a ejecutar el contenedor con:
```bash
$ docker compose up
```
Esto aplicará las migraciones automáticamente.
