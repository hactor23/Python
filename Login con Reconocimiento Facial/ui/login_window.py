from __future__ import annotations

import threading
import tkinter as tk
from tkinter import messagebox

from ..services.auth_service import login, register
from ..db.user_repository import user_exists
from .menu_window import open_menu


def start_login() -> None:
    root = tk.Tk()
    root.title("Login Facial")
    root.geometry("420x300")

    tk.Label(root, text="Usuario", font=("Arial", 12)).pack(pady=(16, 8))
    entry = tk.Entry(root, width=32)
    entry.pack(pady=2)

    status = tk.Label(root, text="", fg="gray")
    status.pack(pady=12)

    def set_status(msg: str) -> None:
        status.config(text=msg)
        root.update_idletasks()

    def set_busy(busy: bool) -> None:
        state = tk.DISABLED if busy else tk.NORMAL
        btn_login.config(state=state)
        btn_register.config(state=state)
        btn_exit.config(state=state)
        entry.config(state=state)

    def run_in_thread(fn, on_done) -> None:
        """
        Ejecuta `fn()` en un hilo y llama `on_done(result)` en el hilo de Tk.
        `fn` debe devolver (ok: bool, msg: str).
        """

        def worker() -> None:
            try:
                result = fn()
            except Exception as e:  # evita que la app muera silenciosamente
                result = (False, f"Error inesperado: {e}")
            root.after(0, lambda: on_done(result))

        threading.Thread(target=worker, daemon=True).start()

    def do_login() -> None:
        username = entry.get().strip()
        if not username:
            messagebox.showwarning("Falta usuario", "Ingresa un nombre de usuario.")
            return

        set_busy(True)
        set_status("Abriendo cámara para verificar...")
        root.update()
        root.withdraw()

        run_in_thread(
            lambda: login(username),
            lambda result: _finish_login(username, result),
        )

    def _finish_login(username: str, result) -> None:
        ok, msg = result
        if ok:
            root.destroy()
            open_menu(username)
            return
        root.deiconify()
        set_status(msg)
        set_busy(False)

    def do_register() -> None:
        username = entry.get().strip()
        if not username:
            messagebox.showwarning("Falta usuario", "Ingresa un nombre de usuario a registrar.")
            return

        set_busy(True)
        set_status("Abriendo cámara para registrar...")
        root.update()
        root.withdraw()

        run_in_thread(
            lambda: register(username),
            lambda result: _finish_register(username, result),
        )

    def _finish_register(username: str, result) -> None:
        ok, msg = result
        root.deiconify()
        if ok:
            # Mostrar el mensaje real del servicio (y verificar persistencia)
            try:
                persisted = user_exists(username)
            except Exception as e:
                messagebox.showerror("Registro", f"{msg}\n\nError verificando DB: {e}")
                set_busy(False)
                return

            if not persisted:
                messagebox.showerror("Registro", f"{msg}\n\nPero NO se encontró el usuario en la base de datos.")
                set_busy(False)
                return

            messagebox.showinfo("Registro", msg)
            # Tras registrar, vamos directo al menú principal.
            root.destroy()
            open_menu(username)
            return
        else:
            messagebox.showerror("Registro", msg)
            set_status(msg)
        set_busy(False)

    btn_login = tk.Button(root, text="Ingresar", width=22, command=do_login)
    btn_login.pack(pady=8)

    btn_register = tk.Button(root, text="Registrar", width=22, command=do_register)
    btn_register.pack(pady=6)

    btn_exit = tk.Button(root, text="Salir", width=22, command=root.destroy)
    btn_exit.pack(pady=18)

    root.mainloop()

