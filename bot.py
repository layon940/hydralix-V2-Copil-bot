from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
from config import BOT_TOKEN, CREATOR_ID
from utils.uploader import upload_video
from utils.progress import generate_progress_bar, get_system_stats
import os, time

queue = []
users = set()

async def start(update: Update, context: CallbackContext):
    users.add(update.effective_user.id)
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("Lo siento solo sirvo a mi amo @layon940")
    else:
        await update.message.reply_text("¡Bienvenido, amo! Estoy listo para servirte.")

async def ayuda(update: Update, context: CallbackContext):
    await update.message.reply_text("Este bot acepta archivos de video y los sube a un servidor. Solo funciona para @layon940.")

async def ads(update: Update, context: CallbackContext):
    if update.effective_user.id != CREATOR_ID:
        return
    await update.message.reply_text("Envía el mensaje que deseas difundir.")

    def confirm_message(msg):
        keyboard = [
            [InlineKeyboardButton("Sí", callback_data="send_ads"),
             InlineKeyboardButton("No", callback_data="cancel_ads")]
        ]
        return InlineKeyboardMarkup(keyboard)

    context.user_data["ads_pending"] = True

async def handle_message(update: Update, context: CallbackContext):
    if context.user_data.get("ads_pending") and update.effective_user.id == CREATOR_ID:
context.user_data["ads_message"] = update.message.text
        context.user_data["ads_pending"] = False
        await update.message.reply_text("¿Deseas enviar este anuncio?", reply_markup=confirm_message(update.message.text))

async def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    if query.data == "send_ads":
        msg = context.user_data.get("ads_message")
        for i, uid in enumerate(users):
            try:
                await context.bot.send_message(chat_id=uid, text=msg)
                await query.edit_message_text(f"Enviando... {i+1}/{len(users)}")
                time.sleep(10)
            except:
                continue
        await query.edit_message_text("Difusión completada.")
    elif query.data == "cancel_ads":
        await query.edit_message_text("Anuncio cancelado.")

async def video_handler(update: Update, context: CallbackContext):
    if update.effective_user.id != CREATOR_ID:
        return
    video = update.message.video or update.message.document
    if video and video.mime_type.startswith("video/"):
        file = await context.bot.get_file(video.file_id)
        path = f"./downloads/{video.file_name}"
        await file.download_to_drive(path)
        queue.append(path)
        await update.message.reply_text(f"Archivo añadido a la cola: {video.file_name}")
        if len(queue) == 1:
            await process_queue(update, context)

async def process_queue(update: Update, context: CallbackContext):
    while queue:
        current = queue[0]
        # Simular progreso
        for i in range(0, 101, 5):
            bar = generate_progress_bar(i)
            cpu, ram, free = get_system_stats()
            await update.message.reply_text(
                f"┌ {os.path.basename(current)}\n"
                f"├ {bar}\n"
                f"├ Progreso: {i}%\n"
                f"├ Tamaño: {round(os.path.getsize(current)/(1024**2),2)}MB\n"
                f"├ Velocidad: 1.2MB/s\n"
                f"├ ETA: {int((100-i)/510)}s\n"
                f"├ Transcurrido: {i0.1:.1f}s\n"
                f"├ Acción: Subida\n"
                f"└——————————————————\n"
                f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n"
                f"CPU: {cpu}% | RAM: {ram}% | FREE: {free}GB"
            )
            time.sleep(10)
        upload_video(current)
        queue.pop(0)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("ads", ads))
app.add_handler(MessageHandler(filters.TEXT & filters.USER(CREATOR_ID), handle_message))
app.add_handler(MessageHandler(filters.VIDEO | filters.Document.VIDEO, video_handler))
app.add_handler(MessageHandler(filters.ALL, handle_message))
app.add_handler(MessageHandler(filters.ALL, handle_callback))

app.run_polling()
