import requests
import os
import sys

def upload_video(file_path, upload_url):
    if not os.path.isfile(file_path):
        print(f"❌ El archivo '{file_path}' no existe.")
        return

    file_name = os.path.basename(file_path)
    file_type = 'video/mp4'  # Puedes ajustar esto si usas otros formatos

    try:
        with open(file_path, 'rb') as f:
            files = { 'file': (file_name, f, file_type) }
            print(f"📤 Subiendo '{file_name}' a {upload_url}...")
            response = requests.post(upload_url, files=files)

        if response.status_code == 200:
            print("✅ Subida exitosa:")
            print(response.text)
        else:
            print(f"⚠️ Error en la subida. Código: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"🚨 Ocurrió un error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python uploader.py <ruta_del_video> <url_de_subida>")
    else:
        file_path = sys.argv[1]
        upload_url = sys.argv[2]
        upload_video(file_path, upload_url)
