# Login Facial Web (Flask)

Sistema web con:

- Registro e ingreso facial desde la cámara del navegador
- Menú con **Control de accesos** (historial del usuario actual) y **Reportes** (eventos por día, todos los usuarios)
- SQLite en `data/database.db`

## Instalar

Desde `facial_login_web_flask`:

```bash
pip install -r facial_login_web_flask/requirements.txt
```

## Desarrollo

```bash
python facial_login_web_flask/app.py
```

Abrí `http://127.0.0.1:5000/` (por defecto host `127.0.0.1`, puerto `5000`).

### Variables de entorno útiles

| Variable | Descripción |
|----------|-------------|
| `FLASK_SECRET_KEY` | Clave para firmar cookies de sesión. **Obligatoria en producción** (valor fijo); si no se define, cambia en cada arranque. |
| `FLASK_DEBUG` | `1` / `true` para modo debug (no usar en producción). |
| `FLASK_HOST` | Host de escucha (por defecto `127.0.0.1`). |
| `PORT` | Puerto (por defecto `5000`). |
| `ADMIN_USERNAMES` | Lista separada por comas (ej. `admin,ariel`). Si **está vacía**, cualquier usuario logueado puede ver **Reportes**. Si **definís usuarios**, solo ellos ven reportes globales; el resto verá un aviso al entrar. |
| `REGISTER_SAMPLES` | Fotos requeridas en el registro (por defecto `5`). |
| `FACE_TOLERANCE` | Tolerancia de comparación (por defecto `0.5`). |

## Producción (Windows)

El servidor de desarrollo de Flask no es adecuado para exponer en red. Usá **Waitress**:

```bash
cd facial_login_web_flask
waitress-serve --listen=0.0.0.0:5000 wsgi:application
```

Definí antes `FLASK_SECRET_KEY` y, si hace falta, `PORT`.

### HTTPS y cámara

Los navegadores suelen exigir **HTTPS** (o `localhost`) para acceder a la cámara si no es `127.0.0.1`. En producción lo habitual es poner **Nginx**, **Caddy** o **IIS** delante con TLS y hacer proxy a Waitress en `127.0.0.1:5000`.

## Notas

- La base de datos es un archivo local; hacé copias de seguridad de `data/database.db` si la usás en serio.
