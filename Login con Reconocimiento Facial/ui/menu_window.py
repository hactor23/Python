from __future__ import annotations

import tkinter as tk
from tkinter import messagebox

from .access_window import open_access_window
from .reports_window import open_reports_window


def open_menu(username: str) -> None:
    root = tk.Tk()
    root.title("Menú Principal")
    root.geometry("430x330")

    tk.Label(root, text=f"Bienvenido {username}", font=("Arial", 14)).pack(pady=18)

    tk.Button(
        root,
        text="Control de Accesos",
        width=28,
        command=lambda: open_access_window(root, username),
    ).pack(pady=6)
    tk.Button(
        root,
        text="Reportes",
        width=28,
        command=lambda: open_reports_window(root, username),
    ).pack(pady=6)
    tk.Button(root, text="Configuración", width=28, command=lambda: messagebox.showinfo("Configuración", "Aquí podrías ajustar parámetros del sistema.")).pack(pady=6)

    tk.Button(root, text="Cerrar sesión", width=28, command=root.destroy).pack(pady=18)

    root.mainloop()

