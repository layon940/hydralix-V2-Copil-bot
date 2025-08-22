import os
import mimetypes
import requests

def upload_video(file_path):
    api_id = os.getenv("HYDRAX_API_ID")
    if not api_id:
        raise ValueError("❌ HYDRAX_API_ID no está configurado en las variables de entorno.")

    url = f"http://up.hydrax.net/{api_id}"
    file_name = os.path.basename(file_path)
    file_type = mimetypes.guess_type(file_name)[0] or 'video/mp4'

    with open(file_path, 'rb') as f:
        files = {'file': (file_name, f, file_type)}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        return f"Subida exitosa:\n{response.text}"
    else:
        return f"Error en la subida. Código: {response.status_code}\n{response.text}"
