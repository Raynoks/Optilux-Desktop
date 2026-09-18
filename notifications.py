"""
Notifications bureau (Windows). Utilise windows-toasts (qui passe par
ToastNotificationManager, l'API WinRT) — le nom et l'icône affichés sur le
toast sont déterminés par l'AppUserModelID du processus, défini dans app.py
via SetCurrentProcessExplicitAppUserModelID.
"""
import threading
import os


APP_NAME = "OPTILUX"


def notify(title, message, timeout=8, icon_path=None):
    def _send():
        try:
            from windows_toasts import WindowsToaster, Toast, ToastDisplayImage, ToastImagePosition
        except ImportError:
            print("[notifications] windows-toasts introuvable")
            return
        try:
            toaster = WindowsToaster(APP_NAME)
            toast = Toast()
            toast.text_fields = [title, message]
            toaster.show_toast(toast)
        except Exception as e:
            print(f"[notification indisponible] {title} — {message} ({e})")

    threading.Thread(target=_send, daemon=True).start()