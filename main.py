import os
import time
import schedule
from telegram import Bot
from datetime import datetime

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_ping():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bot.send_message(chat_id=CHAT_ID, text=f"✅ Тест: бот активен! Сейчас {now}")

schedule.every(1).minutes.do(send_ping)

print("🔁 Бот запущен в тестовом режиме: сообщение каждую минуту.")

while True:
    schedule.run_pending()
    time.sleep(5)
