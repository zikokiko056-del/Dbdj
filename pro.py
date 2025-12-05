#!/usr/bin/env python3
# coding: utf-8

import os
import sqlite3
import requests
import uuid
from pytube import YouTube
import instaloader
from moviepy.editor import VideoFileClip

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, filters
)

# ---------------- CONFIG ----------------
ADMIN_ID = 8431804711
TOKEN = "8438096029:AAFLuBsLxIxKoI9umE2-4dGx6QJ67OOrmkM"   # <-- ضع التوكن هنا
TMP_VIDEO = "downloaded_video.mp4"

ASK_URL = 1
ASK_PARTS = 2

# ---------------- DB ----------------
DB_PATH = "bot_admin.db"

def db_connect():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            uses INTEGER DEFAULT 0,
            limit_count INTEGER DEFAULT 3,
            vip INTEGER DEFAULT 0,
            banned INTEGER DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            url TEXT,
            parts INTEGER,
            status TEXT DEFAULT 'pending', -- pending / approved / rejected / processed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# User helpers
def add_user(user_id, username):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE id=?", (user_id,))
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users (id, username) VALUES (?,?)", (user_id, username))
        conn.commit()
    conn.close()

def get_user(user_id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id, username, uses, limit_count, vip, banned FROM users WHERE id=?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row

def inc_user_uses(user_id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET uses = uses + 1 WHERE id=?", (user_id,))
    conn.commit()
    conn.close()

def grant_uses(user_id, n):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET uses = uses - ? WHERE id=?", ( -n, user_id))  # decrease uses count to give allowance
    conn.commit()
    conn.close()

def set_vip(user_id, val=1):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET vip=? WHERE id=?", (1 if val else 0, user_id))
    conn.commit()
    conn.close()

def ban_user(user_id, val=1):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE users SET banned=? WHERE id=?", (1 if val else 0, user_id))
    conn.commit()
    conn.close()

# Requests helpers
def create_request(user_id, username, url, parts):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO requests (user_id, username, url, parts) VALUES (?,?,?,?)", (user_id, username, url, parts))
    req_id = cur.lastrowid
    conn.commit()
    conn.close()
    return req_id

def get_request(req_id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id, user_id, username, url, parts, status FROM requests WHERE id=?", (req_id,))
    row = cur.fetchone()
    conn.close()
    return row

def update_request_status(req_id, status):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("UPDATE requests SET status=? WHERE id=?", (status, req_id))
    conn.commit()
    conn.close()

# ---------------- Downloaders ----------------
def download_youtube(url, out_path=TMP_VIDEO):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    stream.download(filename=out_path)
    return out_path

def download_instagram(url, out_path=TMP_VIDEO):
    # Note: For public posts only.
    L = instaloader.Instaloader()
    shortcode = url.rstrip("/").split("/")[-1]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    # prefer direct video_url
    video_url = getattr(post, "video_url", None)
    if not video_url:
        for node in post.get_sidecar_nodes():
            if node.is_video:
                video_url = node.video_url
                break
    if not video_url:
        raise Exception("No video found in the Instagram post.")
    r = requests.get(video_url, stream=True)
    with open(out_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return out_path

# ---------------- Video split ----------------
def split_video_file(input_path, parts):
    clip = VideoFileClip(input_path)
    duration = clip.duration
    seg = duration / parts
    out_files = []
    for i in range(parts):
        start = i * seg
        end = min((i+1)*seg, duration)
        out_name = f"part_{uuid.uuid4().hex[:8]}_{i+1}.mp4"
        sub = clip.subclip(start, end)
        sub.write_videofile(out_name, codec="libx264", audio_codec="aac", verbose=False, logger=None)
        out_files.append(out_name)
    clip.close()
    return out_files

# ---------------- Bot handlers ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username or "")
    await update.message.reply_text("👋 سير فحال! صيفط ليا رابط ديال الفيديو (YouTube أو Instagram) باش نبدأ.")

async def handle_url_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    # store URL and ask for parts
    context.user_data["pending_url"] = text
    await update.message.reply_text("🔢 شحال من جزء بغيتي نقسم الفيديو عليه؟ (مثال: 3)")
    return ASK_PARTS

async def handle_parts_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    username = user.username or ""
    # check user status
    add_user(uid, username)
    row = get_user(uid)
    if row:
        _, _, uses, limit_count, vip, banned = row
    else:
        uses = 0; limit_count = 3; vip = 0; banned = 0

    if banned:
        await update.message.reply_text("❌ أنت ممنوع من استعمل البوت.")
        return ConversationHandler.END

    try:
        parts = int(update.message.text.strip())
        url = context.user_data.get("pending_url")
        if not url:
            await update.message.reply_text("❌ ماوصلني حتى رابط. رجع أرسل الرابط.")
            return ConversationHandler.END

        # create request
        req_id = create_request(uid, username, url, parts)

        # notify admin with inline buttons
        kb = [
            [
                InlineKeyboardButton("✅ Approve & Process", callback_data=f"approve:{req_id}"),
                InlineKeyboardButton("❌ Reject", callback_data=f"reject:{req_id}")
            ],
            [
                InlineKeyboardButton("➕ Grant 1", callback_data=f"grant:{req_id}:1"),
                InlineKeyboardButton("➕ Grant 3", callback_data=f"grant:{req_id}:3"),
                InlineKeyboardButton("⭐ Make VIP", callback_data=f"vip:{req_id}")
            ]
        ]
        text = f"📩 New request #{req_id}\nFrom: @{username} (ID: {uid})\nURL: {url}\nParts: {parts}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=text, reply_markup=InlineKeyboardMarkup(kb))

        await update.message.reply_text("✅ الطلب توصل للأدمن. في انتظار الموافقة.")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ: {e}")

    return ConversationHandler.END

# ---------------- Callback handlers for admin actions ----------------
async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = query.from_user

    # only admin may press action buttons
    if user.id != ADMIN_ID:
        return await query.edit_message_text("❌ غير الأدمن عندو الحق يدير هاد العملية.")

    try:
        parts = data.split(":")
        action = parts[0]

        if action == "approve":
            req_id = int(parts[1])
            req = get_request(req_id)
            if not req:
                return await query.edit_message_text("❌ الطلب ما لقيتوهش.")
            _, uid, uname, url, parts_num, status = req
            if status != "pending":
                return await query.edit_message_text(f"🚫 الحالة الحالية: {status}")

            await query.edit_message_text(f"⏳ Approved request #{req_id}. Processing...")
            update_request_status(req_id, "approved")

            # process (download + split + send)
            try:
                # check banned again
                u = get_user(uid)
                if u and u[5] == 1:
                    update_request_status(req_id, "rejected")
                    await context.bot.send_message(chat_id=uid, text="❌ تم رفض طلبك (محظور).")
                    return

                # download
                if "youtube" in url or "youtu.be" in url:
                    download_youtube(url, TMP_VIDEO)
                elif "instagram" in url:
                    download_instagram(url, TMP_VIDEO)
                else:
                    await context.bot.send_message(chat_id=uid, text="❌ الرابط غير مدعوم.")
                    update_request_status(req_id, "rejected")
                    return

                # split
                out_files = split_video_file(TMP_VIDEO, parts_num)

                # send files to user
                for fpath in out_files:
                    await context.bot.send_video(chat_id=uid, video=open(fpath, "rb"))
                    os.remove(fpath)

                os.remove(TMP_VIDEO)
                update_request_status(req_id, "processed")
                inc_user_uses(uid)
                await context.bot.send_message(chat_id=uid, text=f"✅ طلبك #{req_id} تَزوّد وبْعثت ليك المقاطع.")
            except Exception as e:
                update_request_status(req_id, "rejected")
                await context.bot.send_message(chat_id=ADMIN_ID, text=f"❌ خطأ أثناء معالجة #{req_id}: {e}")
                await context.bot.send_message(chat_id=uid, text="❌ وقع خطأ أثناء معالجة طلبك.")
            return

        elif action == "reject":
            req_id = int(parts[1])
            req = get_request(req_id)
            if not req:
                return await query.edit_message_text("❌ الطلب ما لقيتوهش.")
            _, uid, _, _, _, status = req
            update_request_status(req_id, "rejected")
            await context.bot.send_message(chat_id=uid, text=f"❌ طلب #{req_id} تم رفضه من الأدمن.")
            return await query.edit_message_text(f"❌ Request #{req_id} rejected.")

        elif action == "grant":
            req_id = int(parts[1])
            n = int(parts[2])
            req = get_request(req_id)
            if not req:
                return await query.edit_message_text("❌ الطلب ما لقيتوهش.")
            _, uid, _, _, _, _ = req
            # grant n uses: we can decrease 'uses' to give allowance (or raise limit_count)
            conn = db_connect()
            cur = conn.cursor()
            cur.execute("UPDATE users SET uses = uses - ? WHERE id=?", (-n, uid))  # uses = uses + n -> but because the code checks uses >= limit, simplest is to reduce uses
            conn.commit()
            conn.close()
            await context.bot.send_message(chat_id=uid, text=f"✅ الأدمن عطاك {n} استعمال إضافي.")
            return await query.edit_message_text(f"➕ Granted {n} uses to {uid} (request #{req_id}).")

        elif action == "vip":
            req_id = int(parts[1])
            req = get_request(req_id)
            if not req:
                return await query.edit_message_text("❌ الطلب ما لقيتوهش.")
            _, uid, _, _, _, _ = req
            set_vip(uid, 1)
            await context.bot.send_message(chat_id=uid, text=f"🌟 الأدمن عطاك VIP — استعمال غير محدود.")
            return await query.edit_message_text(f"⭐ User {uid} set to VIP (request #{req_id}).")
    except Exception as e:
        await query.edit_message_text(f"❌ خطأ داخلي: {e}")

# ---------------- Admin commands (manage users) ----------------
async def users_cmd(update: Update, ctx):
    if update.effective_user.id != ADMIN_ID:
        return
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT id, username, uses, limit_count, vip, banned FROM users")
    rows = cur.fetchall()
    conn.close()
    text = "📜 Users:\n"
    for r in rows:
        text += f"ID:{r[0]} @{r[1]} uses:{r[2]} limit:{r[3]} VIP:{r[4]} banned:{r[5]}\n"
    await update.message.reply_text(text)

async def ban_cmd(update: Update, ctx):
    if update.effective_user.id != ADMIN_ID: return
    try:
        uid = int(update.message.text.split()[1])
        ban_user(uid, 1)
        await update.message.reply_text(f"⛔ Banned {uid}")
    except:
        await update.message.reply_text("Usage: /ban <id>")

async def unban_cmd(update: Update, ctx):
    if update.effective_user.id != ADMIN_ID: return
    try:
        uid = int(update.message.text.split()[1])
        ban_user(uid, 0)
        await update.message.reply_text(f"✔️ Unbanned {uid}")
    except:
        await update.message.reply_text("Usage: /unban <id>")

async def setvip_cmd(update: Update, ctx):
    if update.effective_user.id != ADMIN_ID: return
    try:
        uid = int(update.message.text.split()[1])
        set_vip(uid, 1)
        await update.message.reply_text(f"⭐ {uid} is now VIP")
    except:
        await update.message.reply_text("Usage: /setvip <id>")

async def removevip_cmd(update: Update, ctx):
    if update.effective_user.id != ADMIN_ID: return
    try:
        uid = int(update.message.text.split()[1])
        set_vip(uid, 0)
        await update.message.reply_text(f"❌ VIP removed from {uid}")
    except:
        await update.message.reply_text("Usage: /removevip <id>")

# ---------------- Conversation & main ----------------
def main():
    init_db()
    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url_entry)],
            ASK_PARTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_parts_entry)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(callback_query_handler))

    # admin commands
    app.add_handler(CommandHandler("users", users_cmd))
    app.add_handler(CommandHandler("ban", ban_cmd))
    app.add_handler(CommandHandler("unban", unban_cmd))
    app.add_handler(CommandHandler("setvip", setvip_cmd))
    app.add_handler(CommandHandler("removevip", removevip_cmd))

    print("🤖 Bot running (admin-enabled)...")
    app.run_polling()

if __name__ == "__main__":
    main()