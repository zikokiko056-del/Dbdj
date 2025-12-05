#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import uuid
import asyncio
import logging
from functools import partial
from yt_dlp import YoutubeDL
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ================================
# ⚠️ ADMIN SETTINGS
# ================================
ADMIN_ID = 8431804711  # ← إنت الإدمن هنا
TOKEN = "8438096029:AAFLuBsLxIxKoI9umE2-4dGx6QJ67OOrmkM"

BOT_ACTIVE = True
BANNED_USERS = set()

TMP_DIR = "downloads"
os.makedirs(TMP_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# --------------------------------------------------
# Detect Platform
# --------------------------------------------------

def detect_platform(url: str) -> str:
    url = url.lower()
    if "youtu" in url: return "YouTube"
    if "insta" in url: return "Instagram"
    if "facebook" in url or "fb.watch" in url: return "Facebook"
    if "tiktok" in url: return "TikTok"
    if "twitter" in url or "x.com" in url: return "Twitter"
    if "reddit" in url: return "Reddit"
    return "Unknown"


# --------------------------------------------------
# yt-dlp Download System
# --------------------------------------------------

def ytdlp_block(url, kind, cookiesfile=None):
    base = uuid.uuid4().hex
    outtmpl = os.path.join(TMP_DIR, base + ".%(ext)s")

    # Video or Audio
    if kind == "mp4":
        opts = {
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
        }
    else:
        opts = {
            "format": "bestaudio",
            "outtmpl": outtmpl,
            "quiet": True,
            "noplaylist": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }],
        }

    if cookiesfile:
        opts["cookiefile"] = cookiesfile

    with YoutubeDL(opts) as ydl:
        ydl.extract_info(url, download=True)

    # get produced file
    files = [f for f in os.listdir(TMP_DIR) if f.startswith(base)]
    files.sort(key=lambda f: os.path.getctime(os.path.join(TMP_DIR, f)))
    return os.path.join(TMP_DIR, files[-1])


async def download_async(url, kind, cookiesfile=None):
    loop = asyncio.get_event_loop()
    func = partial(ytdlp_block, url, kind, cookiesfile)
    return await loop.run_in_executor(None, func)


# --------------------------------------------------
# BOT HANDLERS
# --------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.id in BANNED_USERS:
        return await update.message.reply_text("🚫 تم حظرك من استخدام البوت.")

    keyboard = [
        [KeyboardButton("YouTube"), KeyboardButton("Instagram")],
        [KeyboardButton("Facebook"), KeyboardButton("TikTok")],
        [KeyboardButton("Twitter/X"), KeyboardButton("Reddit")],
    ]
    await update.message.reply_text(
        "👋 مرحبا! أرسل رابط أي فيديو وسأعطيك خيارات MP3 / MP4.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE

    user = update.message.from_user

    if user.id in BANNED_USERS:
        return await update.message.reply_text("🚫 تم حظرك من استخدام البوت.")

    if not BOT_ACTIVE and user.id != ADMIN_ID:
        return await update.message.reply_text("⛔ البوت غير مفعل الآن. تواصل مع الإدمن.")

    text = update.message.text.strip()

    # user selected platform
    if text.lower() in ["youtube", "instagram", "facebook", "tiktok", "twitter/x", "reddit"]:
        context.user_data["expected_platform"] = text
        await update.message.reply_text(f"✔️ جيد! الآن أرسل رابط {text}.")
        return

    # assume it's a URL
    url = text
    platform = detect_platform(url)

    context.user_data["url"] = url

    # notify admin
    if user.id != ADMIN_ID:
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📥 استعمال جديد:\n👤 {user.first_name}\n🆔 {user.id}\n🔗 {url}"
            )
        except:
            pass

    # options
    buttons = [
        [
            InlineKeyboardButton("🎬 تحميل MP4", callback_data="mp4"),
            InlineKeyboardButton("🎵 تحميل MP3", callback_data="mp3"),
        ],
        [InlineKeyboardButton("📄 إضافة Cookies (اختياري)", callback_data="cookies")]
    ]

    await update.message.reply_text(
        f"🔗 الرابط: {platform}\nاختر نوع التحميل:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user = query.from_user

    if user.id in BANNED_USERS:
        return await query.message.reply_text("🚫 تم حظرك من استخدام البوت.")

    data = query.data
    url = context.user_data.get("url")

    if not url:
        return await query.message.reply_text("❌ المرجو إرسال الرابط أولا.")

    if data == "cookies":
        context.user_data["awaiting_cookies"] = True
        return await query.message.reply_text("📄 أرسل ملف cookies.txt الآن.")

    kind = "mp4" if data == "mp4" else "mp3"

    await query.edit_message_text("⏳ جاري التحميل...")

    try:
        cookiesfile = context.user_data.get("cookiesfile")
        file_path = await download_async(url, kind, cookiesfile)
    except Exception as e:
        return await query.message.reply_text(f"❌ خطأ أثناء التحميل:\n{e}")

    try:
        if file_path.endswith(".mp3"):
            await query.message.reply_audio(audio=open(file_path, "rb"))
        else:
            await query.message.reply_video(video=open(file_path, "rb"))
    except:
        await query.message.reply_document(document=open(file_path, "rb"))

    try:
        os.remove(file_path)
    except:
        pass


async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_cookies"):
        doc = update.message.document
        if not doc:
            return await update.message.reply_text("❌ هذا ليس ملفاً.")

        newpath = os.path.join(TMP_DIR, "cookies_" + uuid.uuid4().hex + ".txt")
        await doc.get_file().download_to_drive(newpath)

        context.user_data["cookiesfile"] = newpath
        context.user_data["awaiting_cookies"] = False

        await update.message.reply_text("✔️ تم حفظ الكوكيز.\nالآن اختر MP3 أو MP4.")


# --------------------------------------------------
# ADMIN COMMANDS
# --------------------------------------------------

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    buttons = [
        [InlineKeyboardButton("🚫 Ban User", callback_data="admin_ban")],
        [InlineKeyboardButton("✔️ Unban User", callback_data="admin_unban")],
        [InlineKeyboardButton("⛔ إيقاف البوت", callback_data="admin_off")],
        [InlineKeyboardButton("✅ تشغيل البوت", callback_data="admin_on")],
    ]

    await update.message.reply_text("⚙️ *لوحة التحكم*", 
                                    reply_markup=InlineKeyboardMarkup(buttons), 
                                    parse_mode="Markdown")


async def admin_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global BOT_ACTIVE
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return await query.message.reply_text("❌ غير مسموح")

    data = query.data

    # Turn OFF bot
    if data == "admin_off":
        BOT_ACTIVE = False
        return await query.message.reply_text("⛔ تم إيقاف البوت.")

    # Turn ON bot
    if data == "admin_on":
        BOT_ACTIVE = True
        return await query.message.reply_text("✅ تم تشغيل البوت.")

    # Ban user
    if data == "admin_ban":
        context.user_data["admin_action"] = "ban"
        return await query.message.reply_text("🛑 أرسل ID ديال المستخدم باش نحظرو.")

    # Unban user
    if data == "admin_unban":
        context.user_data["admin_action"] = "unban"
        return await query.message.reply_text("🔓 أرسل ID ديال المستخدم باش نفكّ الحظر.")


async def admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    action = context.user_data.get("admin_action")
    if not action:
        return

    try:
        uid = int(update.message.text.strip())
    except:
        return await update.message.reply_text("❌ ID غير صالح")

    if action == "ban":
        BANNED_USERS.add(uid)
        await update.message.reply_text(f"🚫 تم حظر المستخدم: {uid}")

    elif action == "unban":
        if uid in BANNED_USERS:
            BANNED_USERS.remove(uid)
        await update.message.reply_text(f"🔓 تم فك الحظر عن: {uid}")

    context.user_data["admin_action"] = None


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # main bot
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(admin_buttons, pattern="admin_"))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, file_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, admin_text))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 البوت شغال...")
    app.run_polling()


if __name__ == "__main__":
    main()