import os
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from telegram import Bot
from datetime import datetime
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
EMAIL = os.environ.get("BOOKING_EMAIL")
PASSWORD = os.environ.get("BOOKING_PASSWORD")

bot = Bot(token=BOT_TOKEN)

async def notify(text):
    await bot.send_message(chat_id=CHAT_ID, text=text)

async def run():
    await notify("🚀 Начинаю тест бронирования!")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://clubspark.lta.org.uk/PrioryPark2/Booking")

        # Войти
        login_btn = driver.find_element(By.XPATH, "//a[contains(text(),'Sign in')]")
        login_btn.click()
        time.sleep(2)

        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[contains(text(),'Sign in')]").click()
        time.sleep(3)

        await notify("✅ Авторизация прошла успешно.")

        # Пролистываем ближайшие дни
        days_checked = 0
        booked = False
        while days_checked < 7 and not booked:
            time.sleep(3)
            slots = driver.find_elements(By.CLASS_NAME, "booking-slot.available")
            for slot in slots:
                text = slot.text.lower()
                if "16:00" in text or "08:00" in text or "15:00" in text or "09:00" in text:
                    slot.click()
                    await notify("🎾 Нашёл доступный слот: " + text + " — тест клик выполнен!")
                    booked = True
                    break
            if not booked:
                next_day = driver.find_element(By.XPATH, "//button[contains(@class,'navigate-next')]")
                next_day.click()
                days_checked += 1

        if not booked:
            await notify("😕 Свободных слотов не найдено.")

    except Exception as e:
        await notify("❌ Ошибка в процессе: " + str(e))
    finally:
        driver.quit()

asyncio.run(run())
