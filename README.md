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