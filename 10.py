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
    ReplyKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# ================= إعدادات البوت =================

TOKEN = "8365323089:AAFNhje1rkW3nMUUrT1y8GaYOvoeA-cC_MM"

# 👇 هنا الأدمن (أنت)
ADMINS = [8431804711]

TMP_DIR = "downloads"
os.makedirs(TMP_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =====================================================


def detect_platform(url: str) -> str:
    url = url.lower()
    if "youtu" in url: return "YouTube"
    if "insta" in url: return "Instagram"
    if "facebook" in url or "fb.watch" in url: return "Facebook"
    if "tiktok" in url: return "TikTok"
    if "twitter" in url or "x.com" in url: return "Twitter"
    if "reddit" in url: return "Reddit"
    return "Unknown"


# ================= yt-dlp ==================

def ytdlp_block(url, kind, cookiesfile=None):
    base = uuid.uuid4().hex
    outtmpl = os.path.join(TMP_DIR, base + ".%(ext)s")

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

    files = [f for f in os.listdir(TMP_DIR) if f.startswith(base)]
    files.sort(key=lambda f: os.path.getctime(os.path.join(TMP_DIR, f)))
    return os.path.join(TMP_DIR, files[-1])


async def download_async(url, kind, cookiesfile=None):
    loop = asyncio.get_event_loop()
    func = partial(ytdlp_block, url, kind, cookiesfile)
    return await loop.run_in_executor(None, func)


# ================= Handlers ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id

    keyboard = [
        [KeyboardButton("YouTube"), KeyboardButton("Instagram")],
        [KeyboardButton("Facebook"), KeyboardButton("TikTok")],
        [KeyboardButton("Twitter/X"), KeyboardButton("Reddit")],
    ]

    # زرّ خاص بالأدمن فقط
    if user in ADMINS:
        keyboard.append([KeyboardButton("⚙️ لوحة التحكم")])

    await update.message.reply_text(
        "👋 مرحبا! أرسل رابط أي فيديو وسأعطيك MP3 أو MP4.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user = update.effective_user.id

    if text == "⚙️ لوحة التحكم":
        if user not in ADMINS:
            return await update.message.reply_text("❌ غير مسموح لك.")

        return await update.message.reply_text(
            "⚙️ لوحة الأدمن:\n• مراقبة المستخدمين\n• التحكم بالكويكز\n• إدارة الروابط"
        )

    # إذا كتب اسم منصة
    if text.lower() in ["youtube", "instagram", "facebook", "tiktok", "twitter/x", "reddit"]:
        context.user_data["expected_platform"] = text
        return await update.message.reply_text(f"✔️ زوين! دابا صيفط الرابط ديال {text}.")

    # نعتبره رابط
    url = text
    context.user_data["url"] = url
    platform = detect_platform(url)

    buttons = [
        [
            InlineKeyboardButton("🎬 تحميل MP4", callback_data="mp4"),
            InlineKeyboardButton("🎵 MP3 تحميل", callback_data="mp3"),
        ],
        [InlineKeyboardButton("📄 Cookies", callback_data="cookies")]
    ]

    await update.message.reply_text(
        f"🔗 المنصة: {platform}\nاختار نوع التحميل:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    url = context.user_data.get("url")
    if not url:
        return await query.message.reply_text("❌ صيفط الرابط أولاً.")

    if data == "cookies":
        context.user_data["awaiting_cookies"] = True
        return await query.message.reply_text("📄 صيفط ملف cookies.txt")

    kind = "mp4" if data == "mp4" else "mp3"
    await query.edit_message_text("⏳ جاري التحميل...")

    try:
        file_path = await download_async(url, kind, context.user_data.get("cookiesfile"))
    except Exception as e:
        return await query.message.reply_text(f"❌ خطأ:\n{e}")

    # إرسال
    try:
        if file_path.endswith(".mp3"):
            await query.message.reply_audio(open(file_path, "rb"))
        else:
            await query.message.reply_video(open(file_path, "rb"))
    except:
        await query.message.reply_document(open(file_path, "rb"))

    os.remove(file_path)


async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_cookies"):
        doc = update.message.document
        if not doc:
            return await update.message.reply_text("❌ خاص ملف!")

        newpath = os.path.join(TMP_DIR, f"cookies_{uuid.uuid4().hex}.txt")
        await doc.get_file().download_to_drive(newpath)

        context.user_data["cookiesfile"] = newpath
        context.user_data["awaiting_cookies"] = False

        await update.message.reply_text("✔️ تم حفظ الكوكيز! دابا اختار MP3 أو MP4.")


# ================= Main ==================

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, file_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 البوت شغّال...")
    app.run_polling()


if __name__ == "__main__":
    main()