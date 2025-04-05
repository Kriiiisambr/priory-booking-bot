import os
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot
from datetime import datetime
import time

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
USERNAME = os.environ.get("BOOKING_USERNAME")
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
        driver.get("https://clubspark.lta.org.uk/PrioryPark2/Booking/BookByDate#?date=2025-04-05&role=guest")
        
        # Нажимаем кнопку "Sign in"
        sign_in_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Sign in')]"))
        )
        sign_in_btn.click()

        # Нажимаем на красную кнопку "Log in"
        login_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Log in')]"))
        )
        login_btn.click()

        # Вводим username и password
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        driver.find_element(By.NAME, "username").send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)

        # Нажимаем на синюю кнопку "Log in"
        driver.find_element(By.XPATH, "//button[contains(text(),'Log in')]").click()

        await notify("✅ Авторизация прошла успешно.")
        time.sleep(4)

        # Дальше по коду для выбора слота
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
