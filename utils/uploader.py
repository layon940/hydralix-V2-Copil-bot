import os
import mimetypes
import requests
import time
import logging

LOG_FILENAME = "hydralix.log"

def log_event(msg):
    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )
    logging.info(msg)

def upload_video_with_speed(file_path):
    api_id = os.getenv("HYDRAX_API_ID")
    if not api_id:
        log_event("❌ HYDRAX_API_ID no está configurado en las variables de entorno.")
        raise ValueError("❌ HYDRAX_API_ID no está configurado en las variables de entorno.")

    url = f"http://up.hydrax.net/{api_id}"
    file_name = os.path.basename(file_path)
    file_type = mimetypes.guess_type(file_name)[0] or 'video/mp4'

    log_event(f"📤 Intentando subir '{file_name}' a Hydrax...")

    try:
        start = time.time()
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f, file_type)}
            response = requests.post(url, files=files)
        end = time.time()
        elapsed = end - start if end > start else 1
        file_size = os.path.getsize(file_path)
        upload_speed = file_size / elapsed if elapsed else file_size
        # Formatear velocidad
        if upload_speed < 1024:
            upload_speed_fmt = f"{upload_speed:.2f} B/s"
        elif upload_speed < 1024 ** 2:
            upload_speed_fmt = f"{upload_speed / 1024:.2f} KB/s"
        elif upload_speed < 1024 ** 3:
            upload_speed_fmt = f"{upload_speed / (1024 ** 2):.2f} MB/s"
        else:
            upload_speed_fmt = f"{upload_speed / (1024 ** 3):.2f} GB/s"

        if response.status_code == 200:
            log_event(f"✅ Subida exitosa de '{file_name}'. Respuesta: {response.text} | Velocidad real: {upload_speed_fmt}")
            return f"Subida exitosa:\n{response.text}", upload_speed_fmt
        else:
            log_event(f"⚠️ Error en la subida de '{file_name}'. Código: {response.status_code}. Respuesta: {response.text} | Velocidad real: {upload_speed_fmt}")
            return f"Error en la subida. Código: {response.status_code}\n{response.text}", upload_speed_fmt
    except Exception as e:
        log_event(f"❌ Excepción subida '{file_name}': {str(e)}")
        return f"Excepción al subir: {str(e)}", "N/A"
