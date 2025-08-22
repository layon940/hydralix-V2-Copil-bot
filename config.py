import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID"))
API_ID = int(os.getenv("API_ID"))     # my.telegram.org api_id
API_HASH = os.getenv("API_HASH")      # my.telegram.org api_hash
PYRO_SESSION = "large_session"        # nombre del archivo de sesión pyrogram
