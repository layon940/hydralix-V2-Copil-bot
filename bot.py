import os
import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from config import BOT_TOKEN, CREATOR_ID
from utils.uploader import upload_video
from utils.progress import generate_progress_bar, get_system_stats

# Configuración logging
LOG_FILENAME = "hydralix.log"
logging.basicConfig(
    filename=LOG_FILENAME,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

queue = []
processing = False
users = set()

def log_event(msg):
    logging.info(msg)

# ===================== Comandos =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users.add(update.effective_user.id)
    log_event(f"/start by user {update.effective_user.id}")
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("Lo siento solo sirvo a mi amo @layon940")
    else:
        await update.message.reply_text("¡Bienvenido, amo! Estoy listo para servirte.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event("/ayuda command")
    await update.message.reply_text(
        "Hydralix acepta archivos de video (mp4, mkv, avi, etc) y los sube a un servidor externo. "
        "Solo funciona para @layon940.\n\n"
        "Comandos disponibles:\n"
        "/start - Inicia el bot\n"
        "/ayuda - Explicación general\n"
        "/ads - Envío de anuncios a todos los usuarios\n"
        "/log - Envía el archivo de log actual\n"
    )

async def ads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event(f"/ads by user {update.effective_user.id}")
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("Solo el creador puede usar este comando.")
        return
    await update.message.reply_text("Envía el mensaje que deseas difundir.")
    context.user_data["ads_pending"] = True

async def send_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    log_event(f"/log by user {update.effective_user.id}")
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("Solo el creador puede usar este comando.")
        return
    if os.path.exists(LOG_FILENAME):
        await update.message.reply_document(document=open(LOG_FILENAME, "rb"))
        log_event("Archivo de log enviado por Telegram")
    else:
        await update.message.reply_text("No existe archivo de log.")

# ===================== Manejo de Mensajes =====================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Para anuncios
    if context.user_data.get("ads_pending") and update.effective_user.id == CREATOR_ID:
        context.user_data["ads_message"] = update.message.text
        context.user_data["ads_pending"] = False
        log_event(f"Mensaje de anuncio recibido: {update.message.text}")
        keyboard = [
            [
                InlineKeyboardButton("Sí", callback_data="send_ads"),
                InlineKeyboardButton("No", callback_data="cancel_ads")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("¿Deseas enviar este anuncio?", reply_markup=reply_markup)

# ===================== Callback para anuncios =====================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "send_ads":
        msg = context.user_data.get("ads_message", "")
        log_event(f"Enviando anuncio: {msg}")
        if not msg:
            await query.edit_message_text("No hay mensaje para enviar.")
            return
        success = 0
        blocked = 0
        total = len(users)
        status_msg = await query.edit_message_text(f"Enviando anuncio a {total} usuarios...")
        for idx, uid in enumerate(users):
            try:
                await context.bot.send_message(chat_id=uid, text=msg)
                success += 1
            except Exception:
                blocked += 1
            # Actualiza cada 10 envíos
            if (idx+1) % 10 == 0 or idx == total-1:
                await status_msg.edit_text(
                    f"Enviando anuncio...\n"
                    f"Enviados: {success}/{total}\n"
                    f"Bloqueados: {blocked}\n"
                )
                await asyncio.sleep(10)
        await status_msg.edit_text(
            f"✅ Difusión completada.\n"
            f"Recibieron: {success}/{total}\n"
            f"Bloqueados: {blocked}"
        )
        log_event(f"Anuncio enviado. Recibieron: {success}. Bloqueados: {blocked}")
    elif query.data == "cancel_ads":
        await query.edit_message_text("Anuncio cancelado.")
        log_event("Anuncio cancelado.")

# ===================== Manejo universal de videos y documentos de video =====================

async def video_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("Solo el creador puede subir videos.")
        log_event(f"Intento de subida por usuario no autorizado: {update.effective_user.id}")
        return

    # Detectar si el mensaje tiene video o documento
    video = update.message.video
    document = update.message.document

    # Procesar video nativo de Telegram
    if video:
        file_id = video.file_id
        file_name = video.file_name or f"{video.file_id}.mp4"
        file_size = video.file_size
        mime_type = video.mime_type
    # Procesar documento que sea video por mime o por extensión
    elif document:
        file_id = document.file_id
        file_name = document.file_name or f"{document.file_id}.mp4"
        file_size = document.file_size
        mime_type = document.mime_type
        # Verifica por mime y/o extensión
        if not (mime_type and mime_type.startswith("video/")):
            if not file_name.lower().endswith(('.mp4','.mkv','.avi','.mov','.webm')):
                await update.message.reply_text("Este archivo no es un video soportado.")
                log_event(f"Archivo no soportado: {file_name} ({mime_type})")
                return
    else:
        await update.message.reply_text("No se detectó video ni documento de video en el mensaje.")
        log_event("No se detectó video ni documento de video en el mensaje recibido.")
        return

    os.makedirs("./downloads", exist_ok=True)
    path = f"./downloads/{file_name}"

    try:
        file = await context.bot.get_file(file_id)
        await file.download_to_drive(path)
        queue.append({
            "path": path,
            "name": file_name,
            "size": file_size
        })
        await update.message.reply_text(f"Archivo añadido a la cola: {file_name}")
        log_event(f"Archivo añadido a la cola: {file_name} ({file_size} bytes)")
        if not processing:
            asyncio.create_task(process_queue(context, update))
    except Exception as e:
        await update.message.reply_text(f"Error descargando el archivo: {str(e)}")
        log_event(f"Error descargando el archivo {file_name}: {str(e)}")

# ===================== Procesador de cola =====================

async def process_queue(context, update):
    global processing
    processing = True
    while queue:
        current = queue[0]
        filename = current["name"]
        path = current["path"]
        size = current["size"]
        # Mensaje de estado
        status_msg = await update.message.reply_text(f"Comenzando subida de {filename}...")
        log_event(f"Comenzando subida de {filename}")
        # Simulación de progreso
        for i in range(0, 101, 5):
            bar = generate_progress_bar(i)
            cpu, ram, free = get_system_stats()
            await status_msg.edit_text(
                f"┌ {filename}\n"
                f"├ {bar}\n"
                f"├ Progreso: {i}%\n"
                f"├ Tamaño: {round(size/(1024**2),2)}MB\n"
                f"├ Velocidad: ~1.2MB/s\n"
                f"├ ETA: {int((100-i)/5)}s\n"
                f"├ Transcurrido: {i*0.1:.1f}s\n"
                f"├ Acción: Subida\n"
                f"└——————————————————\n"
                f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"CPU: {cpu}% | RAM: {ram}% | FREE: {free}GB"
            )
            await asyncio.sleep(1)
        # Subida real
        try:
            resp = upload_video(path)
            await status_msg.edit_text(f"✅ Subida completada: {filename}\n{resp}")
            log_event(f"Subida completada: {filename} | Respuesta: {resp}")
        except Exception as e:
            await status_msg.edit_text(f"❌ Error al subir {filename}: {str(e)}")
            log_event(f"Error al subir {filename}: {str(e)}")
        queue.pop(0)
    processing = False

# ===================== Configuración de Handlers universales =====================

# Handler para videos nativos
video_filters = filters.VIDEO

# Handler para documentos con mime de video
doc_video_mimes = [
    "video/mp4",
    "video/x-matroska",
    "video/x-msvideo",
    "video/quicktime",
    "video/webm"
]
doc_video_filters = filters.Document.MimeType(doc_video_mimes[0])
for mime in doc_video_mimes[1:]:
    doc_video_filters |= filters.Document.MimeType(mime)

# Handler para documentos por extensión
doc_ext_filters = filters.Document.FileExtension("mp4")
for ext in ["mkv", "avi", "mov", "webm"]:
    doc_ext_filters |= filters.Document.FileExtension(ext)

# Handler final que acepta cualquier video/documento de video
universal_video_filter = video_filters | doc_video_filters | doc_ext_filters

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("ads", ads))
app.add_handler(CommandHandler("log", send_log))
app.add_handler(MessageHandler(filters.TEXT & filters.User(CREATOR_ID), handle_message))
app.add_handler(CallbackQueryHandler(handle_callback))
app.add_handler(MessageHandler(universal_video_filter, video_handler))

app.run_polling()
