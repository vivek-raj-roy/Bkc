import time
import psutil
from pyrogram import Client, filters
from pyrogram.types import Message

# Bot Config
API_ID = 7988735
API_HASH = "8339b7684eb7f4653ed032d4828ebf89"
BOT_TOKEN = "5854864826:AAE5oKcLlXAu0uyTjo0NQhXqIZCFbS06fok"

bot = Client("MyBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Start Command
@bot.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    await message.reply_text(
        "**👋 Hey!**\n\n"
        "🤖 I'm a utility bot to assist you!\n\n"
        "**🔗 Join our updates channel:**\n"
        "👉 [BotX Hub](https://t.me/botxhub)\n\n"
        "__Use the buttons below to get started!__",
        disable_web_page_preview=True
    )

# Ping Command
@bot.on_message(filters.command("ping") & filters.private)
async def ping(client: Client, message: Message):
    start = time.time()
    m = await message.reply("🏓 Pinging...")
    end = time.time()
    latency = (end - start) * 1000
    await m.edit(f"🏓 **Pong!**\n⏱️ `{latency:.2f} ms`")

# Status Command
@bot.on_message(filters.command("status") & filters.private)
async def status(client: Client, message: Message):
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    await message.reply_text(
        "**📊 System Status:**\n\n"
        f"🖥️ **CPU Usage:** `{cpu}%`\n"
        f"💾 **RAM Usage:** `{ram}%`\n"
        f"🗂️ **Disk Usage:** `{disk}%`"
    )

# Start the bot
print("Bot is running...")
bot.run()
