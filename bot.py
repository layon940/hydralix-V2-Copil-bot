import os
import asyncio
import logging
import time
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters, ConversationHandler
)
from telegram.error import TelegramError
from pyrogram import Client as PyroClient
from pyrogram.errors.exceptions import PhoneCodeInvalid, PhoneCodeExpired
from config import BOT_TOKEN, CREATOR_ID, API_ID, API_HASH, PYRO_SESSION
from utils.progress import generate_progress_bar, get_system_stats, format_size, format_speed

# --- Conversation states ---
ASK_PHONE, ASK_CODE = range(2)

# ... (rest of tu código de arriba) ...

# ========== COMANDO /create_session AUTOMATIZADO ==========

async def create_session_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != CREATOR_ID:
        await update.message.reply_text("Solo el creador puede usar este comando.")
        return ConversationHandler.END
    await update.message.reply_text("Por favor, envíame tu número de teléfono (con código de país, ejemplo: +34611223344):")
    return ASK_PHONE

async def create_session_ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text.strip()
    context.user_data["phone"] = phone
    await update.message.reply_text("Perfecto. Ahora espera el código de Telegram y envíamelo aquí.")
    context.user_data["client"] = PyroClient(
        PYRO_SESSION,
        api_id=API_ID,
        api_hash=API_HASH,
        phone_number=phone,
        workdir="."
    )
    try:
        await asyncio.to_thread(context.user_data["client"].connect)
        sent_code = await asyncio.to_thread(context.user_data["client"].send_code_request, phone)
    except Exception as e:
        await update.message.reply_text(f"Error solicitando código: {str(e)}")
        return ConversationHandler.END
    return ASK_CODE

async def create_session_ask_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip()
    phone = context.user_data["phone"]
    client = context.user_data["client"]
    try:
        await asyncio.to_thread(client.sign_in, phone, code)
        await asyncio.to_thread(client.disconnect)
        await update.message.reply_text("¡Sesión creada correctamente y guardada como 'large_session.session'! Ya puedes usar el bot.")
    except PhoneCodeInvalid:
        await update.message.reply_text("El código es inválido. Ejecuta /create_session de nuevo.")
    except PhoneCodeExpired:
        await update.message.reply_text("El código expiró. Ejecuta /create_session de nuevo.")
    except Exception as e:
        await update.message.reply_text(f"Error creando la sesión: {str(e)}")
    return ConversationHandler.END

async def create_session_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sesión cancelada.")
    return ConversationHandler.END

create_session_handler = ConversationHandler(
    entry_points=[CommandHandler("create_session", create_session_start)],
    states={
        ASK_PHONE: [MessageHandler(filters.TEXT & filters.User(CREATOR_ID), create_session_ask_phone)],
        ASK_CODE: [MessageHandler(filters.TEXT & filters.User(CREATOR_ID), create_session_ask_code)],
    },
    fallbacks=[CommandHandler("cancel", create_session_cancel)],
    allow_reentry=True
)

# ========== Agrega el handler de conversación ==========
app.add_handler(create_session_handler)

# ... (resto de tus handlers y app.run_polling()) ...
