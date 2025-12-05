import os
import openai
from moviepy.editor import VideoFileClip
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ChatAction

# ------------------------
# 🔑 API KEYS
# ------------------------
TELEGRAM_BOT_TOKEN = "8438096029:AAFLuBsLxIxKoI9umE2-4dGx6QJ67OOrmkM"
openai.api_key = os.getenv("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")

# ------------------------
# 📌 START
# ------------------------
def start(update, context):
    update.message.reply_text(
        "🔥 مرحبا! صيفط ليا فيديو أو صورة، وغادي نعطيك:\n"
        "✔ Caption\n✔ Hashtags\n✔ Keywords\n✔ Title\n✔ تحليل المحتوى\n\n"
        "✨ دابا صيفط أول فيديو!"
    )

# ------------------------
# ⚙ معالجة الفيديو
# ------------------------
def process_video(file_path):
    clip = VideoFileClip(file_path)
    audio_path = file_path.replace(".mp4", ".mp3")
    clip.audio.write_audiofile(audio_path)
    return audio_path

# ------------------------
# 🤖 OpenAI معالجة الملف
# ------------------------
def analyze_content(file_path):
    with open(file_path, "rb") as f:
        resp = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": "حلل هذا الفيديو أو الصورة وأعطني:\n"
                                                       "- Caption قوي\n"
                                                       "- 20 Hashtags Viral\n"
                                                       "- 20 Keywords\n"
                                                       "- Title احترافي\n"
                                                       "- تحليل المحتوى"},
                        {"type": "input_file", "file": f},
                    ],
                },
            ],
        )

    return resp.choices[0].message['content']

# ------------------------
# 📥 استقبال الفيديو والصور
# ------------------------
def handle_media(update, context):
    update.message.reply_chat_action(ChatAction.TYPING)

    # ----- فيديو -----
    if update.message.video:
        file_id = update.message.video.file_id
        file = context.bot.get_file(file_id)
        file_path = "video.mp4"
        file.download(file_path)

        # تحويل MP3
        audio_path = process_video(file_path)

        # تحليل
        update.message.reply_text("⏳ كنعالج الفيديو…")
        result = analyze_content(file_path)

        update.message.reply_text("🎬 *التحليل جاهز:*\n\n" + result, parse_mode="Markdown")

        # إرسال MP3
        update.message.reply_audio(audio=open(audio_path, "rb"))

    # ----- صورة -----
    elif update.message.photo:
        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        file_path = "image.jpg"
        file.download(file_path)

        update.message.reply_text("⏳ كنعالج الصورة…")
        result = analyze_content(file_path)

        update.message.reply_text("🖼 *التحليل جاهز:*\n\n" + result, parse_mode="Markdown")


# ------------------------
# ▶ تشغيل البوت
# ------------------------
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.video | Filters.photo, handle_media))

    updater.start_polling()
    print("🤖 Bot is running…")
    updater.idle()


if __name__ == "__main__":
    main()