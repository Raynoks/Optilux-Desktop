"""
Envoi de messages WhatsApp automatisés — GRATUIT, sans clé API ni compte
professionnel Meta. Fonctionne via pywhatkit, qui ouvre WhatsApp Web dans le
navigateur par défaut et y tape/envoie le message automatiquement.

À savoir avant d'utiliser cette fonctionnalité :
- L'ordinateur doit être allumé, connecté à internet, avec WhatsApp Web déjà
  connecté au moins une fois (scan du QR code) — la session reste ensuite active.
- Une fenêtre de navigateur s'ouvre VISIBLEMENT à chaque envoi — ce n'est pas
  silencieux, contrairement aux notifications Windows.
- Ce n'est pas un canal officiel WhatsApp — réservez ceci à des rappels
  ponctuels (un RDV, une commande prête), pas à un envoi en masse, au risque
  d'une limitation temporaire du numéro par WhatsApp.
"""
import threading
import re
import datetime

DEFAULT_COUNTRY_CODE = "+212"  # Maroc


def normalize_phone(phone, default_country_code=DEFAULT_COUNTRY_CODE):
    """Convertit un numéro local marocain (ex. 0612345678) au format international
    requis par WhatsApp (+212612345678). Retourne None si vide/invalide."""
    if not phone:
        return None
    digits = re.sub(r"[^\d+]", "", phone)
    if not digits:
        return None
    if digits.startswith("+"):
        return digits
    if digits.startswith("00"):
        return "+" + digits[2:]
    if digits.startswith("0"):
        return default_country_code + digits[1:]
    return default_country_code + digits


def send_whatsapp(phone, message, wait_seconds=15, close_after=True):
    """Envoie un message WhatsApp en arrière-plan (thread séparé — ne bloque jamais
    l'interface). Retourne True si l'envoi a été lancé (numéro valide), False sinon.
    Le succès réel de l'envoi (le message est bien parti) ne peut pas être confirmé
    de façon synchrone ; les erreurs sont journalisées en console plutôt que de
    faire planter l'application."""
    number = normalize_phone(phone)
    if not number:
        print("[WhatsApp] numéro invalide ou manquant — envoi annulé")
        return False

    def _send():
        try:
            import pywhatkit  # import différé : ne casse jamais le démarrage de l'appli
            pywhatkit.sendwhatmsg_instantly(
                number, message, wait_time=wait_seconds, tab_close=close_after
            )
        except Exception as e:
            print(f"[WhatsApp indisponible] {number} : {message} ({e})")

    threading.Thread(target=_send, daemon=True).start()
    return True
