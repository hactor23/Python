from __future__ import annotations

import time
import warnings
from typing import Iterable, List, Optional, Sequence, Tuple

import cv2
# face_recognition_models (dependencia) dispara un UserWarning por pkg_resources (deprecado).
# No afecta a la app; filtramos solo ese warning para no confundir en consola.
warnings.filterwarnings(
    "ignore",
    message=r"pkg_resources is deprecated as an API\..*",
    category=UserWarning,
)
import face_recognition
import numpy as np

from ..config import (
    CAMERA_INDEX,
    DEDUP_DISTANCE_THRESHOLD,
    MAX_LOGIN_SECONDS,
    MAX_REGISTER_SECONDS,
    REGISTER_SAMPLES,
    PROCESS_EVERY_N_FRAMES,
    TOLERANCE,
)


def _bgr_to_rgb(frame_bgr: np.ndarray) -> np.ndarray:
    # frame[:, :, ::-1] suele quedar con strides negativos (no-contiguo).
    # dlib/face_recognition puede fallar o no detectar bien si la imagen no es contigua.
    rgb = frame_bgr[:, :, ::-1]
    return np.ascontiguousarray(rgb, dtype=np.uint8)


def _normalize_face_locations(face_locations: Iterable[object]) -> List[Tuple[int, int, int, int]]:
    """
    `face_recognition.face_locations` normalmente devuelve (top, right, bottom, left).
    En algunos entornos puede venir algo inesperado; normalizamos y filtramos para
    evitar que `dlib.compute_face_descriptor` crashee.
    """
    normalized: List[Tuple[int, int, int, int]] = []
    for loc in face_locations:
        # loc puede ser tuple/list/np.ndarray
        try:
            items = list(loc)  # type: ignore[arg-type]
        except Exception:
            continue

        if len(items) != 4:
            continue

        try:
            top, right, bottom, left = (int(items[0]), int(items[1]), int(items[2]), int(items[3]))
        except Exception:
            continue

        normalized.append((top, right, bottom, left))
    return normalized


def capture_user_encodings(
    samples_required: int = REGISTER_SAMPLES,
    camera_index: int = CAMERA_INDEX,
) -> Tuple[List[np.ndarray], bool]:
    """
    Captura encodings mientras haya una cara detectable.
    Devuelve: (encodings, cancelado)
    """
    cam = cv2.VideoCapture(camera_index)
    if not cam.isOpened():
        return [], True

    encodings: List[np.ndarray] = []
    start = time.time()
    cancelado = False

    frame_idx = 0
    while len(encodings) < samples_required:
        if time.time() - start > MAX_REGISTER_SECONDS:
            break

        ret, frame = cam.read()
        if not ret:
            continue

        # Render guía rápida (si el procesamiento es pesado,
        # mantener la previsualización responsiva).
        overlay = f"Capturando: {len(encodings)}/{samples_required} | ESC: cancelar"
        cv2.putText(frame, overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Procesa reconocimiento cada N frames para evitar “tirones”
        # (face_recognition es pesado).
        if frame_idx % max(1, PROCESS_EVERY_N_FRAMES) == 0:
            rgb = _bgr_to_rgb(frame)
            raw_locations = face_recognition.face_locations(rgb, model="hog")
            face_locations = _normalize_face_locations(raw_locations)

            if face_locations:
                try:
                    face_encs = face_recognition.face_encodings(rgb, face_locations)
                except TypeError:
                    # En algunos setups, dlib puede recibir argumentos incompatibles
                    # si las locaciones vienen corruptas. No abortamos el registro.
                    face_encs = []
            else:
                face_encs = []

            # Fallback: si no obtuvimos encodings pero hay imagen válida,
            # probamos dejar que face_recognition calcule locaciones internamente.
            if not face_encs:
                try:
                    face_encs = face_recognition.face_encodings(rgb)
                except TypeError:
                    face_encs = []

            # Tomamos la primera cara detectada para simplificar el flujo.
            # Antes se hacía una deduplicación fuerte, lo que a veces dejaba
            # el contador pegado en 1/15. Con menos muestras y sin filtro
            # tan agresivo, el contador avanza de forma más predecible.
            if face_encs:
                encodings.append(face_encs[0])

        frame_idx += 1

        cv2.imshow("Registro facial", frame)

        # Aumenta un poco waitKey para mejorar responsividad de la ventana.
        key = cv2.waitKey(10)
        if key == 27:  # ESC
            cancelado = True
            break

    cam.release()
    cv2.destroyAllWindows()
    return encodings, cancelado


def verify_user_with_camera(
    known_encodings: Sequence[np.ndarray],
    camera_index: int = CAMERA_INDEX,
    tolerance: float = TOLERANCE,
) -> bool:
    if not known_encodings:
        return False

    cam = cv2.VideoCapture(camera_index)
    if not cam.isOpened():
        return False

    start = time.time()
    verified = False

    known_list = list(known_encodings)

    frame_idx = 0
    while time.time() - start < MAX_LOGIN_SECONDS:
        ret, frame = cam.read()
        if not ret:
            continue

        overlay = "Verificando rostro... (ESC: cancelar)"
        cv2.putText(frame, overlay, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        if frame_idx % max(1, PROCESS_EVERY_N_FRAMES) == 0:
            rgb = _bgr_to_rgb(frame)
            raw_locations = face_recognition.face_locations(rgb, model="hog")
            face_locations = _normalize_face_locations(raw_locations)
            if face_locations:
                try:
                    face_encs = face_recognition.face_encodings(rgb, face_locations)
                except TypeError:
                    face_encs = []
            else:
                face_encs = []

            if not face_encs:
                try:
                    face_encs = face_recognition.face_encodings(rgb)
                except TypeError:
                    face_encs = []

            for enc in face_encs:
                matches = face_recognition.compare_faces(known_list, enc, tolerance=tolerance)
                if any(matches):
                    verified = True
                    break

        frame_idx += 1
        cv2.imshow("Ingreso facial", frame)

        key = cv2.waitKey(10)
        if key == 27:  # ESC
            break

        if verified:
            break

    cam.release()
    cv2.destroyAllWindows()
    return verified

