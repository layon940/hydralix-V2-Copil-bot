import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID"))
API_ID = int(os.getenv("API_ID"))     # my.telegram.org api_id
API_HASH = os.getenv("API_HASH")      # my.telegram.org api_hash

# --- NUEVO: Puedes usar session string generado con Pyrogram ---
# Si tienes el string de sesión generado manualmente, pégalo aquí:
PYRO_SESSION_STRING = os.getenv("PYRO_SESSION_STRING", "")

# Si dejas PYRO_SESSION_STRING vacío, el bot usará el archivo .session
PYRO_SESSION_FILE = "large_session"        # nombre del archivo de sesión pyrogram

# El bot usará PYRO_SESSION_STRING si está presente, si no usará PYRO_SESSION_FILE.session
