# Agora — Blog & Oráculo (Django)

Proyecto web en **Django** que combina un **blog** con gestión de publicaciones e imágenes, una app de **cuentas** (registro, login y perfil) y un **Oráculo (I‑Ching)** que genera hexagramas, permite **exportar a PDF** y **enviar resultados por correo**.

> Este README entrega una guía completa para desarrollar, ejecutar y desplegar el proyecto de forma segura.

---

## ✨ Características principales
- **Blog**: CRUD de publicaciones con imagen, listado, detalle y administración desde Django Admin.
- **Cuentas**: registro/inicio de sesión, perfil de usuario con avatar (subida a `media/`).
- **Oráculo (I‑Ching)**: formulario de consulta, generación de hexagramas, **PDF** con ReportLab y **envío por email**.
- **Frontend**: plantillas con **Bootstrap** (base en `templates/base.html`).
- **Base de datos**: **SQLite** por defecto (archivo `db.sqlite3`). Fácil de migrar a Postgres.
- **Archivos**: `media/` para subidas; `static/` y `staticfiles/` para estáticos recolectados.
- **Compatibilidad**: Python 3.10+ y Django 5.x.

---

## 🧱 Estructura del repositorio (simplificada)

```
Agora/
├─ AgoraBlog/                # Proyecto Django (settings, urls, wsgi/asgi)
│  ├─ AgoraBlog/settings.py
│  ├─ AgoraBlog/urls.py
│  ├─ ...
│
├─ blog/                     # App de blog
│  ├─ models.py / views.py / urls.py / templates/blog/
│
├─ accounts/                 # App de usuarios/perfiles
│  ├─ models.py / views.py / forms.py / templates/accounts/
│
├─ oraculo/                  # App I‑Ching (PDF/email)
│  ├─ models.py / views.py / forms.py / templates/oraculo/
│
├─ templates/                # base.html y plantillas compartidas
├─ static/                   # estáticos de desarrollo
├─ media/                    # subidas de usuario (se crea en runtime)
├─ manage.py
├─ requirements.txt          # dependencias del proyecto
└─ .env                      # variables de entorno (NO subir a Git)
```

> **Nota:** No incluyas `.venv/` ni `db.sqlite3` en el repositorio. Usa `.gitignore` (ver abajo).

---

## 📦 Requisitos previos
- **Python 3.10+**
- **pip** y **venv** (o pipenv/poetry si prefieres)
- **Git**
- Opcional: **SQLite** (viene con Python) o **PostgreSQL** para producción
- Para enviar correos con Gmail: habilitar **App Password** (con 2FA activo).

---

## 🚀 Puesta en marcha (local)

1) Clonar y crear entorno virtual
```bash
git clone <URL-de-tu-repo> agora
cd agora
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
```

2) Instalar dependencias
```bash
pip install -r requirements.txt
```

3) Configurar variables de entorno (`.env` en la raíz del proyecto)
```ini
# Seguridad
DJANGO_SECRET_KEY=pon-aqui-una-clave-segura
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

# Email (Gmail con App Password)
EMAIL_HOST_USER=tu-cuenta@gmail.com
EMAIL_HOST_PASSWORD=tu-app-password

# Opcional: base de datos Postgres
# DATABASE_URL=postgres://usuario:pass@host:5432/nombre_db
```

4) Migraciones y superusuario
```bash
python manage.py migrate
python manage.py createsuperuser
```

5) Ejecutar el servidor
```bash
python manage.py runserver
# http://127.0.0.1:8000/
```

---

## ⚙️ Configuración importante (settings)

En `AgoraBlog/settings.py` se recomienda cargar valores desde el entorno:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-inseguro')
DEBUG = os.getenv('DJANGO_DEBUG', '') == '1'
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Archivos estáticos y media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Email (Gmail)
- Activa **2FA** en tu cuenta.
- Genera un **App Password** y colócalo en `EMAIL_HOST_PASSWORD`.
- El **remitente (`from_email`)** debe coincidir con `EMAIL_HOST_USER` para evitar bloqueos SPF/DMARC.

### Base de datos
Por defecto usa SQLite (`db.sqlite3`). Para Postgres, usa `DATABASE_URL` con `dj-database-url` o configura `DATABASES` manualmente.

---

## 🧭 Rutas y apps

- **Home / Blog**
  - `GET /` listado (home)
  - `GET /blog/` listado de publicaciones
  - `GET /blog/<slug|id>/` detalle de publicación
  - CRUD bajo vistas protegidas o Django Admin

- **Cuentas**
  - `GET/POST /accounts/login/`, `/accounts/signup/`, `/accounts/logout/`
  - `/accounts/profile/` ver/editar perfil (avatar en `media/`)

- **Oráculo (I‑Ching)**
  - `GET/POST /oraculo/` realizar consulta
  - `POST /oraculo/pdf/` exportar PDF del resultado
  - `POST /oraculo/email/` enviar por correo

> Las rutas exactas pueden variar según `urls.py`; ajusta este README si renombras endpoints.

---

## 🧪 Tests
Si aún no hay tests, puedes iniciar con:
```bash
python manage.py test
```
Recomendación: crear `tests/` por app (`blog/tests/test_models.py`, etc.).

---

## 🧰 Desarrollo en PyCharm / VS Code

**PyCharm**
1. *Run → Edit Configurations…* → **Django server**.
2. `Settings:` ruta a `AgoraBlog/settings.py`  
   `Manage script:` ruta a `manage.py`  
   `Working directory:` la carpeta raíz del proyecto.
3. Ejecuta. **No** corras archivos sueltos (p. ej. `oraculo/views.py`).

**VS Code**
- Extensión *Python* y *Django*.
- Tareas para `runserver`, `migrate`, etc.

---

## 📁 Archivos estáticos y media

- Durante desarrollo, Django sirve estáticos y media.
- En producción:
  - Ejecuta `python manage.py collectstatic` → se vuelcan a `STATIC_ROOT`.
  - Sirve **staticfiles** desde el servidor web o **WhiteNoise**.
  - **Media** (subidas) debe ir a un bucket o volumen persistente.

---

## ☁️ Despliegue (resumen)
- `DEBUG=0`
- `ALLOWED_HOSTS=tu-dominio.com`
- Servidor de aplicaciones: **gunicorn**/**uvicorn** + **nginx** (o usar **WhiteNoise** para estáticos simples).
- Variables de entorno seguras (no subir `.env`).
- `python manage.py migrate && python manage.py collectstatic --noinput`

---

## 🔒 Seguridad
- **No subas** `SECRET_KEY`, `.env`, `db.sqlite3`, ni credenciales al repositorio.
- Usa **HTTPS** en producción.
- Limita tamaño de archivo y tipos permitidos en `MEDIA` (validaciones en formularios).
- Mantén dependencias actualizadas (renueva `requirements.txt`).

---

## 🧯 Errores frecuentes y soluciones

### 1) `ImportError: attempted relative import with no known parent package`
Sucede al ejecutar un archivo suelto (p. ej. `oraculo/views.py`).  
**Solución:** usa `python manage.py runserver` o cambia imports a absolutos (`from oraculo.forms import ...`).

### 2) `RelatedObjectDoesNotExist: User has no profile`
Ocurre si se accede a `request.user.profile` y no existe el `Profile`.  
**Soluciones:**
- En vistas: `profile, _ = Profile.objects.get_or_create(user=request.user)`.
- O reactivar la señal `post_save` para crear/asegurar el perfil al crear usuarios.

### 3) Autor por defecto en publicaciones
Si el modelo `Publicacion` usa un `default` frágil para `autor`, se rompe si no existe ese usuario.  
**Solución:** asigna `publicacion.autor = request.user` antes de guardar y elimina el `default` del modelo.

### 4) Duplicidad de rutas `''` en `blog/urls.py`
Puede causar confusión.  
**Solución:** deja **una** ruta `''` (por ejemplo `name='home'`) y reutiliza ese nombre en plantillas.

### 5) Envío de correos bloqueado por el proveedor
Suele pasar si el `from_email` no coincide con `EMAIL_HOST_USER`.  
**Solución:** usa el mismo correo en ambos campos y App Password con 2FA.

---

## 🗺️ Roadmap / TODOs sugeridos
- [ ] Mover **SECRET_KEY** y credenciales de correo a **variables de entorno** (si no se hizo).
- [ ] Asegurar **creación automática de Profile** con señal `post_save`.
- [ ] Eliminar `default` de `autor` en `Publicacion` y asignar en la vista.
- [ ] Unificar rutas del `blog` y revisar nombres (`name`) en templates.
- [ ] Añadir **tests** básicos (modelo `Publicacion`, vistas de `oraculo`, forms de `accounts`).
- [ ] Configurar **WhiteNoise/nginx** para producción y pipeline de deploy.
- [ ] Añadir CI simple (GitHub Actions) para `flake8` + `pytest`.
- [ ] Documentar endpoints exactos en este README cuando queden definitivos.

---

## 🧾 .gitignore recomendado

```
# Python
__pycache__/
*.py[cod]
*.sqlite3

# Virtualenv
.venv/
env/
venv/

# Django
/staticfiles/
/media/
*.log

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/

# Otros
__MACOSX/
```

---

## 📜 Licencia
Define la licencia de tu preferencia (p. ej. MIT). Si no incluyes licencia, por defecto **todos los derechos reservados**.

---

## 👤 Créditos
**Proyecto Agora** — Django + Bootstrap + ReportLab.
