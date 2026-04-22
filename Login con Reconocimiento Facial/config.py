from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Carpeta donde guardamos la base de datos (SQLite)
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "database.db"

# Configuración de reconocimiento facial
TOLERANCE = 0.5  # umbral de comparación (bajar = más estricto)
# 15 muestras hacía el registro muy largo y a veces se quedaba en 1/15.
# Con 5 muestras el flujo es más ágil y suficiente para un login doméstico.
REGISTER_SAMPLES = 5  # cuántas "buenas" capturas/encodings guardar al registrar
MAX_REGISTER_SECONDS = 45  # timeout para registro
MAX_LOGIN_SECONDS = 25  # timeout para login

# Deduplicación (evita guardar encodings casi idénticos).
# Se mantiene, pero al bajar REGISTER_SAMPLES el usuario ve avanzar el contador.
DEDUP_DISTANCE_THRESHOLD = 0.45

# Para mejorar fluidez: procesar reconocimiento facial cada N frames
PROCESS_EVERY_N_FRAMES = 3

# Cámara por índice (0 = cámara principal)
CAMERA_INDEX = 0

