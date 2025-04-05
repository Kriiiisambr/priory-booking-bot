import os
import time
import schedule
from telegram import Bot

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def send_ping():
    weekday = datetime.utcnow().weekday()
    if weekday in [1, 5]:  # 1 - вторник, 5 - суббота
        bot.send_message(chat_id=CHAT_ID, text="👋 Привет! Сегодня бот на месте и готов к бою 🐾")

# Запуск по вторникам и субботам в 00:05 (UTC, т.е. по Лондону)
schedule.every().tuesday.at("00:05").do(send_ping)
schedule.every().saturday.at("00:05").do(send_ping)

print("✅ Бот запущен и ждёт нужный день...")

while True:
    schedule.run_pending()
    time.sleep(10)
