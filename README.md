# PSI Práctica 3 — SongProject

## Autores

- Alejandro Morillas Parra
- Juan Larrondo Fernández de Córdoba

Aplicación web para el aprendizaje de idiomas mediante canciones.
Backend implementado con Django + Django REST Framework. Base de datos PostgreSQL en neon.tech. Desplegado en render.com.

---

## Despliegue en producción

| | |
|---|---|
| **URL backend** | https://three-songproject-99-2311-2026-v1.onrender.com |
| **API REST** | https://three-songproject-99-2311-2026-v1.onrender.com/api/v1/ |
| **Panel admin** | https://three-songproject-99-2311-2026-v1.onrender.com/admin/ |
| **Base de datos** | neon.tech (ver `backend-p3/.env`) |

> **Nota**: el plan gratuito de render.com apaga el servicio tras 15 min de inactividad. La primera petición puede tardar ~30 segundos en despertar.

---

## Credenciales

| Usuario | Contraseña | Rol |
|---------|-----------|-----|
| `alumnodb` | `alumnodb` | Superusuario / administrador |
| `user1` | `user1password` | Usuario de prueba |
| `user2` | `user2password` | Usuario de prueba |

---

## API REST — Endpoints

Base URL: `https://three-songproject-99-2311-2026-v1.onrender.com/api/v1/`

### Autenticación (Djoser + Token)

| Método | URL | Auth | Descripción |
|--------|-----|------|-------------|
| POST | `token/login/` | No | Obtener token |
| POST | `token/logout/` | Sí | Invalidar token |
| GET | `users/me/` | Sí | Info del usuario autenticado |

### Canciones (sin autenticación)

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `songs/` | Listado paginado (3 por página) |
| GET | `songs/<id>/` | Detalle de una canción |
| GET | `songs/random/` | Canción aleatoria |
| GET | `songs/top/?n=N` | Top N canciones más reproducidas |
| GET | `songs/search/?title=<texto>` | Buscar por título (insensible a mayúsculas) |

### SongUsers (requiere autenticación)

| Método | URL | Descripción |
|--------|-----|-------------|
| GET | `songusers/` | Listar SongUsers del usuario autenticado |
| POST | `songusers/` | Crear SongUser (el campo `user` se obtiene del token) |
| GET | `songusers/<id>/` | Detalle |
| PUT/PATCH | `songusers/<id>/` | Actualizar |
| DELETE | `songusers/<id>/` | Eliminar |

---

## Estructura del proyecto

```
PSI_P3/                    ← raíz del repositorio git
├── .gitignore
├── README.md
└── backend-p3/             ← raíz del proyecto Django
    ├── .env                ← variables de entorno (render.com URL, neon.tech URI, credenciales locales)
    ├── manage.py
    ├── requirements.txt
    ├── makefile
    ├── build.sh            ← script de build para render.com
    ├── start.sh            ← script de arranque para render.com
    ├── media/              ← archivos de audio, LRC e imágenes
    ├── songproject/        ← configuración global Django
    ├── song_models/        ← app de modelos de datos
    ├── api/                ← app de la API REST
    └── api_test_remote/
```

---

## Configuración local

### Requisitos previos
- Python 3.12+
- PostgreSQL con base de datos `songdatabase` y usuario `alumnodb`/`alumnodb`

### Instalación

```bash
cd backend-p3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

El fichero `backend-p3/.env` contiene las variables de entorno para desarrollo local. Ajustar si la configuración de PostgreSQL local es diferente.

### Inicializar la base de datos y poblarla

```bash
cd backend-p3
source venv/bin/activate
python manage.py migrate
python manage.py populate
```

O usando el makefile:

```bash
make update_models
make populate
```

### Arrancar el servidor local

```bash
python manage.py runserver 8000
# o: make runserver
```

La API estará disponible en `http://localhost:8000/api/v1/`.

---

## Tests

Todos los comandos se ejecutan desde `backend-p3/` con el entorno virtual activado.

### Tests de modelos

```bash
python manage.py test song_models
# o: make test_models
```

### Tests de la API

```bash
python manage.py test api
# o: make test_api
```

### Todos los tests + cobertura

```bash
coverage erase
coverage run manage.py test && coverage report -m
# o: make coverage
```

### Test remoto (contra render.com)

```bash
python -m unittest api_test_remote/test_remote.py -v
```

> Asegurarse de que el servidor en render.com está despierto antes de ejecutarlo.

---

## Comandos útiles del makefile

| Comando | Descripción |
|---------|-------------|
| `make runserver` | Inicia el servidor en el puerto 8000 |
| `make update_models` | Genera y aplica migraciones |
| `make populate` | Puebla la BD con canciones y usuarios de prueba |
| `make test_models` | Tests de los modelos |
| `make test_api` | Tests de la API |
| `make coverage` | Tests + informe de cobertura |
| `make flake8` | Comprobación de estilo |
| `make shell` | Consola interactiva Django |
| `make dbshell` | Consola psql |
| `make clear_media` | Elimina archivos de media generados por tests |
