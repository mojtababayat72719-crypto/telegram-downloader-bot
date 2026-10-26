import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import yt_dlp

# خواندن اطلاعات از متغیرهای محیطی هاست (امن و بدون نیاز به کلاب)
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

app = Client("downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_command(client, message: Message):
    await message.reply_text(
        "سلام! 🤖\n"
        "لینک ویدیوی مورد نظرت از اینستاگرام، یوتیوب یا سایت‌های دیگه رو بفرست تا برات دانلود کنم."
    )

@app.on_message(filters.text & ~filters.command("start"))
async def download_media(client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.reply_text("لطفاً یک لینک معتبر بفرست.")
        return

    status_msg = await message.reply_text("⏳ در حال پردازش و دانلود لینک...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
    }

    try:
        os.makedirs("downloads", exist_ok=True)
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        await status_msg.edit_text("📤 در حال ارسال ویدیو به تلگرام...")
        await message.reply_video(video=file_path, caption=f"📥 دانلود شده توسط ربات شما\n🔗 {url}")

        if os.path.exists(file_path):
            os.remove(file_path)
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ خطا در دانلود:\n`{str(e)}`")

print("ربات روشن شد و در حال گوش دادن به پیام‌هاست...")
app.run()
