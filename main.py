"""
STOKA — Sistema de gestión de stock.
Punto de entrada.

Orden de arranque:
1) multiprocessing.freeze_support()  → necesario en el .exe de Windows.
2) SQLite se crea y se siembra si está vacía.
3) Servidor de chat (sockets) en un hilo.
4) Worker de jobs + loop asyncio en hilos daemon.
5) Proceso hijo de estadísticas (Queue + Pipe + Manager).
6) Login Tkinter y luego la ventana principal.
"""
from __future__ import annotations

import multiprocessing as mp
import sys
import traceback

import matplotlib

matplotlib.use("TkAgg")

# Asegura imports tanto en desarrollo como en el .exe
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> None:
    # === AQUÍ SE USA: multiprocessing.freeze_support ===
    # Función: en binarios PyInstaller, el proceso hijo no debe volver a
    # abrir la GUI; freeze_support despacha el worker correctamente.
    mp.freeze_support()

    from database import db
    from gui.login_window import LoginWindow
    from gui.main_window import MainWindow
    from chat.server import start_chat_server
    from utils.concurrency import (
        StatsProcessPool,
        shutdown_event,
        start_asyncio_thread,
        start_job_worker,
        stop_asyncio,
    )

    db.initialize_database()
    start_job_worker()
    start_asyncio_thread()
    # === AQUÍ SE USA: queue.Queue (job_queue) ===
    # Función: el hilo worker ejecuta el chequeo de stock sin bloquear el login.
    from utils.concurrency import job_queue
    from utils import notifications as notif

    job_queue.put({"fn": notif.alert_low_stock})
    try:
        start_chat_server()
    except OSError as exc:
        print(f"[STOKA] Chat server no pudo iniciar: {exc}")

    stats_pool = StatsProcessPool()

    def launch(session) -> None:
        app = MainWindow(session, stats_pool)
        app.mainloop()

    login = LoginWindow(on_success=lambda s: None)
    login.mainloop()
    session = login.session
    if session is not None:
        launch(session)

    shutdown_event.set()
    stop_asyncio()
    stats_pool.close()


if __name__ == "__main__":
    mp.freeze_support()
    try:
        main()
    except Exception:
        traceback.print_exc()
        try:
            input("\nSTOKA se detuvo por un error. Enter para salir…")
        except EOFError:
            pass
        sys.exit(1)
