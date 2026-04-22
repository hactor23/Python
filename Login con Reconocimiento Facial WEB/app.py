from __future__ import annotations

import base64
import secrets
import sqlite3
import time
import warnings
from dataclasses import dataclass
from functools import wraps
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

import config as app_config

# Evita el warning de pkg_resources (no afecta funcionalidad)
warnings.filterwarnings(
    "ignore",
    message=r"pkg_resources is deprecated as an API\..*",
    category=UserWarning,
)
import face_recognition  # noqa: E402


DB_PATH = app_config.DB_PATH
REGISTER_SAMPLES = app_config.REGISTER_SAMPLES
MAX_REGISTER_SECONDS = app_config.MAX_REGISTER_SECONDS
MAX_LOGIN_SECONDS = app_config.MAX_LOGIN_SECONDS
TOLERANCE = app_config.TOLERANCE


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("user"):
            return redirect(url_for("index"))
        return view(*args, **kwargs)

    return wrapped


def create_app() -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.secret_key = app_config.get_secret_key()

    init_db()

    @app.get("/")
    def index():
        if session.get("user"):
            return redirect(url_for("menu"))
        return render_template("index.html")

    @app.get("/menu")
    @login_required
    def menu():
        user = session.get("user")
        return render_template("menu.html", username=user)

    @app.get("/accesos")
    @login_required
    def accesos():
        username = session.get("user") or ""
        rows = get_user_accesses(username, limit=100)
        return render_template("accesos.html", username=username, rows=rows)

    @app.get("/reportes")
    @login_required
    def reportes():
        username = session.get("user") or ""
        if not app_config.can_view_reports(username):
            flash("No tenés permiso para ver los reportes globales.", "error")
            return redirect(url_for("menu"))
        rows = get_access_summary_by_day(days=30, limit_rows=200)
        return render_template("reportes.html", username=username, rows=rows)

    @app.post("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("index"))

    # --------- API: Registro ---------
    @app.post("/api/register/start")
    def api_register_start():
        username = (request.json or {}).get("username", "").strip()
        if not username:
            return jsonify(ok=False, error="Ingresa un nombre de usuario."), 400
        if user_exists(username):
            return jsonify(ok=False, error="El usuario ya existe."), 400

        token = secrets.token_urlsafe(24)
        _PENDING_REG[token] = PendingFlow(
            username=username,
            started_at=time.time(),
            required=REGISTER_SAMPLES,
            encodings=[],
        )
        return jsonify(ok=True, token=token, required=REGISTER_SAMPLES)

    @app.post("/api/register/frame")
    def api_register_frame():
        payload = request.json or {}
        token = (payload.get("token") or "").strip()
        image_b64 = payload.get("image")
        if not token or not image_b64:
            return jsonify(ok=False, error="Faltan datos."), 400

        flow = _PENDING_REG.get(token)
        if not flow:
            return jsonify(ok=False, error="Token inválido o expirado."), 400
        if time.time() - flow.started_at > MAX_REGISTER_SECONDS:
            _PENDING_REG.pop(token, None)
            return jsonify(ok=False, error="Registro expiró. Intenta de nuevo."), 400

        frame = _decode_image(image_b64)
        if frame is None:
            return jsonify(ok=False, error="Imagen inválida."), 400

        encs = _extract_encodings(frame)
        if encs:
            flow.encodings.append(encs[0])

        count = len(flow.encodings)
        if count >= flow.required:
            # Guardar y finalizar
            try:
                create_user(flow.username, flow.encodings)
                log_access(flow.username, "REGISTER")
            except Exception as e:
                _PENDING_REG.pop(token, None)
                return jsonify(ok=False, error=f"No se pudo guardar: {e}"), 500

            _PENDING_REG.pop(token, None)
            session["user"] = flow.username
            return jsonify(ok=True, done=True, count=count)

        return jsonify(ok=True, done=False, count=count, required=flow.required)

    # --------- API: Login ---------
    @app.post("/api/login/start")
    def api_login_start():
        username = (request.json or {}).get("username", "").strip()
        if not username:
            return jsonify(ok=False, error="Ingresa un nombre de usuario."), 400
        if not user_exists(username):
            return jsonify(ok=False, error="Usuario no existe."), 400

        known = get_user_encodings(username)
        if not known:
            return jsonify(ok=False, error="El usuario no tiene facciones registradas."), 400

        token = secrets.token_urlsafe(24)
        _PENDING_LOGIN[token] = PendingLogin(
            username=username,
            started_at=time.time(),
            known_encodings=known,
        )
        return jsonify(ok=True, token=token)

    @app.post("/api/login/frame")
    def api_login_frame():
        payload = request.json or {}
        token = (payload.get("token") or "").strip()
        image_b64 = payload.get("image")
        if not token or not image_b64:
            return jsonify(ok=False, error="Faltan datos."), 400

        flow = _PENDING_LOGIN.get(token)
        if not flow:
            return jsonify(ok=False, error="Token inválido o expirado."), 400
        if time.time() - flow.started_at > MAX_LOGIN_SECONDS:
            _PENDING_LOGIN.pop(token, None)
            return jsonify(ok=False, error="Login expiró. Intenta de nuevo."), 400

        frame = _decode_image(image_b64)
        if frame is None:
            return jsonify(ok=False, error="Imagen inválida."), 400

        encs = _extract_encodings(frame)
        if not encs:
            return jsonify(ok=True, verified=False)

        verified = _verify(encs[0], flow.known_encodings)
        if verified:
            _PENDING_LOGIN.pop(token, None)
            session["user"] = flow.username
            try:
                log_access(flow.username, "LOGIN")
            except Exception:
                pass
            return jsonify(ok=True, verified=True)

        return jsonify(ok=True, verified=False)

    return app


# ------------------ Reconocimiento facial (backend) ------------------
def _decode_image(data_url_or_b64: str) -> Optional[np.ndarray]:
    # Acepta dataURL "data:image/jpeg;base64,...." o base64 puro
    b64 = data_url_or_b64
    if "," in b64 and b64.strip().lower().startswith("data:"):
        b64 = b64.split(",", 1)[1]
    try:
        raw = base64.b64decode(b64, validate=True)
    except Exception:
        return None

    # face_recognition.load_image_file soporta bytes via BytesIO, pero evitamos PIL extra:
    # usamos numpy desde buffer + cv2 si está disponible.
    try:
        import cv2  # lazy import

        arr = np.frombuffer(raw, dtype=np.uint8)
        bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if bgr is None:
            return None
        rgb = bgr[:, :, ::-1]
        return np.ascontiguousarray(rgb, dtype=np.uint8)
    except Exception:
        return None


def _extract_encodings(rgb_frame: np.ndarray) -> List[np.ndarray]:
    # HOG es rápido (CPU). Para más precisión: model="cnn" (requiere más recursos).
    locs = face_recognition.face_locations(rgb_frame, model="hog")
    if not locs:
        return []
    try:
        encs = face_recognition.face_encodings(rgb_frame, locs)
    except TypeError:
        # Fallback: deja que calcule locaciones internamente
        try:
            encs = face_recognition.face_encodings(rgb_frame)
        except TypeError:
            return []
    return list(encs)


def _verify(candidate: np.ndarray, known: List[np.ndarray]) -> bool:
    if not known:
        return False
    matches = face_recognition.compare_faces(known, candidate, tolerance=TOLERANCE)
    return any(matches)


# ------------------ Persistencia (SQLite) ------------------
def _ensure_parent_dir_exists(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    _ensure_parent_dir_exists(DB_PATH)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db() -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                username TEXT PRIMARY KEY,
                encodings BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS access_logs(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                event TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def user_exists(username: str) -> bool:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        return cur.fetchone() is not None
    finally:
        conn.close()


def create_user(username: str, encodings: List[np.ndarray]) -> None:
    import pickle

    conn = get_connection()
    try:
        cur = conn.cursor()
        enc_blob = pickle.dumps(encodings, protocol=pickle.HIGHEST_PROTOCOL)
        cur.execute(
            "INSERT INTO users(username, encodings) VALUES(?, ?)",
            (username, enc_blob),
        )
        conn.commit()
    finally:
        conn.close()


def get_user_encodings(username: str) -> Optional[List[np.ndarray]]:
    import pickle

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT encodings FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if not row:
            return None
        (enc_blob,) = row
        encodings = pickle.loads(enc_blob)
        return [np.asarray(e, dtype=np.float64) for e in encodings]
    finally:
        conn.close()


def log_access(username: str, event: str) -> None:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO access_logs(username, event) VALUES(?, ?)", (username, event))
        conn.commit()
    finally:
        conn.close()


def get_user_accesses(username: str, limit: int = 100) -> List[Tuple[str, str]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT created_at, event
            FROM access_logs
            WHERE username = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (username, limit),
        )
        return [(str(created_at), str(event)) for (created_at, event) in cur.fetchall()]
    finally:
        conn.close()


def get_access_summary_by_day(days: int = 30, limit_rows: int = 200) -> List[Tuple[str, int]]:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT DATE(created_at) as day, COUNT(*) as total
            FROM access_logs
            WHERE datetime(created_at) >= datetime('now', ?)
            GROUP BY day
            ORDER BY day DESC
            LIMIT ?
            """,
            (f"-{int(days)} days", limit_rows),
        )
        return [(str(day), int(total)) for (day, total) in cur.fetchall()]
    finally:
        conn.close()


# ------------------ Estado en memoria (registro/login) ------------------
@dataclass
class PendingFlow:
    username: str
    started_at: float
    required: int
    encodings: List[np.ndarray]


@dataclass
class PendingLogin:
    username: str
    started_at: float
    known_encodings: List[np.ndarray]


_PENDING_REG: Dict[str, PendingFlow] = {}
_PENDING_LOGIN: Dict[str, PendingLogin] = {}


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=app_config.get_host(),
        port=app_config.get_port(),
        debug=app_config.get_debug(),
    )

