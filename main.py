import os
from telegram import Bot
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
bot.send_message(chat_id=CHAT_ID, text=f"📨 Тест: бот может писать! Сейчас {now}")
