import requests

def upload_video(file_path):
    with open(file_path, 'rb') as f:
        response = requests.post(
            "https://api.tuservidordevideo.com/upload",
            files={'file': f}
        )
    return response.json()
