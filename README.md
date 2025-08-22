# Hydralix Bot

**Hydralix** es un bot de Telegram avanzado para manejo y envío de archivos grandes, especialmente videos, usando la librería [Pyrogram](https://docs.pyrogram.org/) como userbot.

## Características principales

- **Recepción y envío de archivos grandes**: El bot recibe videos por Bot API y los reenvía usando Pyrogram, superando el límite de tamaño del Bot API.
- **Configuración flexible de sesión Pyrogram**: Puedes usar un archivo `.session` generado con el comando `/create_session`, o pegar un `session string` generado manualmente en la variable de entorno `PYRO_SESSION_STRING` para máxima portabilidad y seguridad.
- **Comando /create_session**: Permite crear y configurar la sesión de Pyrogram desde el propio bot, guiando al usuario paso a paso para registrar el número de teléfono y código de Telegram.
- **Comando /ping**: Devuelve la IP pública del host, útil para monitoreo externo (ej: UptimeRobot).
- **Comando /log**: Permite descargar el archivo de log del bot.
- **Comando /ads**: Difusión de anuncios a todos los usuarios registrados.
- **Comando /ayuda**: Lista todos los comandos y funciones disponibles.

## Instalación

1. **Clona el repositorio** en Replit, VPS o tu máquina local.
2. **Instala las dependencias**:
    ```
    python-telegram-bot==20.3
    pyrogram
    tgcrypto
    psutil
    requests
    ```
3. **Configura las variables de entorno** en Replit o en tu entorno local:
    - `BOT_TOKEN`: Token de tu bot de BotFather.
    - `CREATOR_ID`: Tu user_id de Telegram.
    - `API_ID` y `API_HASH`: Obtenidos en [my.telegram.org](https://my.telegram.org/apps).
    - Opcional: `PYRO_SESSION_STRING` si generaste manualmente el session string (más seguro y portable).

## Uso

- Ejecuta el bot y usa `/start` para verificar que está activo.
- Para configurar Pyrogram y habilitar el envío de archivos grandes:
    - Ejecuta `/create_session` y sigue las instrucciones enviando tu número de teléfono y el código recibido por Telegram.
    - O bien, ejecuta el script auxiliar para generar el session string y pégalo en la variable de entorno `PYRO_SESSION_STRING`.
- Envía archivos de video y el bot los procesará automáticamente usando Pyrogram como usuario (sin límite de tamaño).
- Usa `/ping` para obtener la IP pública y configurar monitoreo externo.

## Advertencia de seguridad

- El archivo o string de sesión Pyrogram **no debe compartirse** y permite acceso total a la cuenta de Telegram usada.
- Solo el usuario con el `CREATOR_ID` tiene acceso a los comandos avanzados.

## Historial de cambios

- **2025-08-22:** Añadida gestión flexible de sesión Pyrogram (session string o archivo), instrucciones detalladas en README, mejoras de seguridad y robustez, y documentación de variables de entorno.

---

**Hydralix Bot - Powered by Pyrogram & python-telegram-bot**
