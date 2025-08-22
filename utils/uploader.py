import os
import requests

def upload_video(file_path):
    api_id = os.getenv("HYDRAX_API_ID")
    bot_token = os.getenv("BOT_TOKEN")  # Si lo necesitas en este script
    if not api_id:
        raise ValueError("❌ HYDRAX_API_ID no está configurado en las variables de entorno.")
    
    url = f"http://up.hydrax.net/{api_id}"
    file_name = os.path.basename(file_path)
    file_type = 'video/mp4'

    with open(file_path, 'rb') as f:
        files = { 'file': (file_name, f, file_type) }
        print(f"📤 Subiendo '{file_name}' a Hydrax...")
        response = requests.post(url, files=files)

    if response.status_code == 200:
        print("✅ Subida exitosa:")
        print(response.text)
    else:
        print(f"⚠️ Error en la subida. Código: {response.status_code}")
        print(response.text)
