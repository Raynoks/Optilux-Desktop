"""
Notifications bureau (Windows). Utilise plyer, qui pilote les notifications natives
Windows 10/11 (toast) — et se dégrade sans plantage si aucun backend n'est disponible
(ex. en développement sur Linux/Mac sans service de notifications).
Envoyées dans un thread séparé pour ne jamais geler l'interface.
"""
import threading
import os

APP_NAME = "OPTILUX"


def notify(title, message, timeout=8, icon_path=None):
    def _send():
        try:
            from plyer import notification
            kwargs = dict(title=title, message=message, timeout=timeout, app_name=APP_NAME)
            if icon_path and os.path.exists(icon_path):
                kwargs["app_icon"] = icon_path
            notification.notify(**kwargs)
        except Exception as e:
            # Pas de backend disponible (ex. hors Windows, ou service de notifications
            # désactivé) — on ne casse jamais l'application pour ça.
            print(f"[notification indisponible] {title} — {message} ({e})")

    threading.Thread(target=_send, daemon=True).start()
