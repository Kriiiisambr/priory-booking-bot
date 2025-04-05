import os
import time
import threading
import schedule
from telegram import Bot
from datetime import datetime
from flask import Flask

# Telegram setup
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
bot = Bot(token=BOT_TOKEN)

# Flask-заглушка
app = Flask(__name__)

@app.route('/')
def home():
    return "🏓 Бот работает!"

def send_ping():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    bot.send_message(chat_id=CHAT_ID, text=f"✅ Тест: бот активен! Сейчас {now}")

def bot_loop():
    schedule.every(1).minutes.do(send_ping)
    while True:
        schedule.run_pending()
        time.sleep(5)

# Бот запускается в фоне
threading.Thread(target=bot_loop, daemon=True).start()

# Flask запускается в основном потоке, чтобы Render не орал
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
