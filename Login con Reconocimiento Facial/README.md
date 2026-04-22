# Facial Login + Menú (SQLite)

App de escritorio (Tkinter) con:
- Login con reconocimiento facial desde la cámara
- Botón para registrar usuarios (captura varias facciones)
- Menú principal con botones

## Requisitos
- `Python 3.x`
- Cámara web

## Instalar dependencias
Desde la carpeta `facial_login_menu`:
```bash
pip install -r requirements.txt
```

## Ejecutar
```bash
# Opción 1 (recomendada, desde `Ejercicios/Python`):
cd "Ejercicios/Python"
python -m facial_login_menu.app

# Opción 2 (también funciona):
cd "facial_login_menu"
python app.py
```

## Uso
1. En el login escribe el `usuario` y pulsa `Registrar`.
2. Se abrirá la cámara y se capturan varias encodings (rostros).
3. Luego escribe el mismo `usuario` y pulsa `Ingresar` para verificar.

Presiona `ESC` en las ventanas de OpenCV para cancelar el flujo.

