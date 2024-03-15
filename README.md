# pidecola_back
Backend de pidecolausb

## Setup inicial
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
### Configuracion de grupos/permisos

En Windows:
```
Get-Content permissions_setup.py | python manage.py shell
```

En Unix:
```
python manage.py shell < permissions_setup.py
```

## Setup con docker

Estando en el directorio del repo, construye la imagen con:
```bash
$ docker compose build
```
Espera a que termine, puede durar, depende de la conexión a internet

Luego, inicia el servicio y la sincronización de los archivos con:
```bash
$ docker compose watch
```
Esto inicia el servidor pero no muestra los logs del programa.
Para ver los logs, abre una nueva terminal, posicionate en el directorio
del código y ejecuta el siguiente comando:
```bash
$ docker compose logs -f
```

Si es la primera vez que ejecutas el programa, debes crear un superuser

### Creación de superuser
Para ejecutar comandos en el contenedor, asegúrate que el contenedor está corriendo.
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

Particularmente, para crear el superuser de django, ejecuta:

``` bash
$ python manage.py createsuperuser
```
Esto te llevará por un proceso interactivo para asignar nombre de usuario y contraseña

Una vez terminado el proceso de creación, puedes salir de la sesión de bash con:
``` bash
$ exit
```

Ya sólo te queda probar la conexión con el servidor. Abre un navegador y visita la siguiente url:
```
http://localhost:8000/admin
```
Escribe las credenciales con las que creaste el superuser para iniciar sesión

Para detener el servicio, ejecuta el siguiente comando el directorio:
``` bash
$ docker compose stop
```
### Lidiando con migraciones en docker
Al hacer cambios en los modelos, debes ejecutar las migraciones.
Por sencillez, basta con que detengas el contenedor de docker y lo
vuelvas a ejecutar para aplicar el cambio.

En la terminal donde ejecutaste `docker compose watch` puedes pulsar `CTRL+C` para detener el servicio watch y
para detener el contenedor escribe:
``` bash
$ docker compose stop
```
Luego, vuelve a ejecutar el contenedor con:
```bash
$ docker compose watch
```
Esto aplicará las migraciones automáticamente.
