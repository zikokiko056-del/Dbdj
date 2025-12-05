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

# ---------------- إعدادات البوت ----------------

TOKEN = "8394415105:AAHnyX8L_i3d1Ug-0C1suv6ucEQAQoXLBYA"
ADMIN_ID = 8431804711  # ⭐ هذا انت

TMP_DIR = "downloads"
os.makedirs(TMP_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# قاعدة بيانات بسيطة
USERS = {}
STATS = {"downloads": 0}

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

# ---------------- yt-dlp Downloader ----------------

def ytdlp_block(url, kind, cookiesfile=None):
    base = uuid.uuid4().hex
    outtmpl = os.path.join(TMP_DIR, base + ".%(ext)s")

    opts = {
        "format": "bestvideo+bestaudio/best" if kind == "mp4" else "bestaudio",
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "quiet": True,
        "noplaylist": True,
    }

    if kind == "mp3":
        opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        }]

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

# ---------------- لوحة التحكم ----------------

async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        return await update.message.reply_text("❌ ليس لديك صلاحية الدخول للوحة التحكم.")

    buttons = [
        [InlineKeyboardButton("📊 عدد التحميلات", callback_data="stats")],
        [InlineKeyboardButton("🚫 حظر مستخدم", callback_data="ban"),
         InlineKeyboardButton("♻️ فك الحظر", callback_data="unban")],
        [InlineKeyboardButton("🗑 مسح التحميلات", callback_data="reset")],
    ]

    await update.message.reply_text(
        "🔧 **لوحة التحكم الخاصة بالأدمين**",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def panel_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return await query.edit_message_text("❌ لا يمكنك!")

    action = query.data

    if action == "stats":
        return await query.edit_message_text(f"📊 إجمالي التحميلات: {STATS['downloads']}")

    if action == "reset":
        STATS["downloads"] = 0
        return await query.edit_message_text("✔ تم مسح التحميلات.")

    if action == "ban":
        await query.edit_message_text("📛 أرسل ID المستخدم لحظره:")
        context.user_data["await_ban"] = True
        return

    if action == "unban":
        await query.edit_message_text("♻️ أرسل ID المستخدم لفك الحظر:")
        context.user_data["await_unban"] = True
        return


# ---------------- Handlers الرئيسية ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    USERS[update.message.from_user.id] = True

    keyboard = [
        [KeyboardButton("YouTube"), KeyboardButton("Instagram")],
        [KeyboardButton("Facebook"), KeyboardButton("TikTok")],
        [KeyboardButton("Twitter/X"), KeyboardButton("Reddit")],
    ]
    await update.message.reply_text(
        "👋 مرحبا! أرسل رابط أي فيديو وسأعطيك خيارات MP3 / MP4.\n\n📌 للأدمين: /panel",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # الحظر
    if user_id in USERS and USERS[user_id] is False:
        return await update.message.reply_text("❌ لقد تم حظرك من استخدام البوت")

    # استقبال ID للحظر
    if context.user_data.get("await_ban"):
        uid = int(update.message.text)
        USERS[uid] = False
        context.user_data["await_ban"] = False
        return await update.message.reply_text(f"🚫 تم حظر المستخدم {uid}")

    # استقبال ID لفك الحظر
    if context.user_data.get("await_unban"):
        uid = int(update.message.text)
        USERS[uid] = True
        context.user_data["await_unban"] = False
        return await update.message.reply_text(f"♻️ تم فك الحظر عن {uid}")

    # رابط الفيديو
    text = update.message.text.strip()
    url = text
    platform = detect_platform(url)

    context.user_data["url"] = url

    buttons = [
        [
            InlineKeyboardButton("🎬 MP4", callback_data="mp4"),
            InlineKeyboardButton("🎵 MP3", callback_data="mp3"),
        ],
        [InlineKeyboardButton("📄 إضافة Cookies", callback_data="cookies")]
    ]

    await update.message.reply_text(
        f"🔗 الرابط: {platform}\nاختر نوع التحميل:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def download_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get("url")
    action = query.data

    if action == "cookies":
        context.user_data["awaiting_cookies"] = True
        return await query.message.reply_text("📄 أرسل ملف cookies.txt الآن.")

    kind = "mp4" if action == "mp4" else "mp3"
    await query.edit_message_text("⏳ جاري التحميل...")

    try:
        cookiesfile = context.user_data.get("cookiesfile")
        file_path = await download_async(url, kind, cookiesfile)
    except Exception as e:
        return await query.message.reply_text(f"❌ خطأ:\n{e}")

    STATS["downloads"] += 1

    # إرسال الملف
    try:
        if file_path.endswith(".mp3"):
            await query.message.reply_audio(audio=open(file_path, "rb"))
        else:
            await query.message.reply_video(video=open(file_path, "rb"))
    except:
        await query.message.reply_document(document=open(file_path, "rb"))

async def cookies_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_cookies"):
        doc = update.message.document

        newpath = os.path.join(TMP_DIR, "cookies_" + uuid.uuid4().hex + ".txt")
        await doc.get_file().download_to_drive(newpath)

        context.user_data["cookiesfile"] = newpath
        context.user_data["awaiting_cookies"] = False

        await update.message.reply_text("✔️ تم حفظ الكوكيز.")

# ---------------- MAIN ----------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("panel", panel))

    app.add_handler(CallbackQueryHandler(panel_buttons, pattern="^(stats|reset|ban|unban)$"))
    app.add_handler(CallbackQueryHandler(download_btn))

    app.add_handler(MessageHandler(filters.Document.ALL, cookies_file))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🤖 البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()