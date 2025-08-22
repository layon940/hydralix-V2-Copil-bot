import os
from pyrogram import Client
from datetime import datetime

def main():
    print("=== Hydralix Pyrogram Session String Creator ===")
    print("Regístrate para obtener tu api_id y api_hash en: https://my.telegram.org/apps\n")

    api_id = input("Introduce tu api_id: ").strip()
    api_hash = input("Introduce tu api_hash: ").strip()
    phone_number = input("Introduce tu número de teléfono (formato internacional, ejemplo: +34611223344): ").strip()

    session_name = input("Nombre para guardar la sesión (por defecto: hydralix_session): ").strip() or "hydralix_session"

    client = Client(session_name, api_id=api_id, api_hash=api_hash, phone_number=phone_number)

    print("\n[!] Te llegará un código de Telegram al teléfono o a la app. Ingresa el código cuando se te pida.")

    try:
        client.start()
        print("\n[+] Sesión iniciada correctamente.")
        session_string = client.export_session_string()
        with open(f"{session_name}_string.txt", "w") as f:
            f.write(session_string)
        print(f"\n[+] Cadena de sesión guardada en {session_name}_string.txt")
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        client.send_message(
            "me",
            f"<b>Session created on: </b>{dt_string}\n\n<code>{session_string}</code>\n\n"
            f"⚠️<b>Guarda este código y NO LO COMPARTAS.</b>⚠️"
        )
        print("[+] También se envió la cadena a tus mensajes guardados en Telegram.")
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        client.stop()

if __name__ == "__main__":
    main()
