"""
whatsapp_sender.py
-------------------
Responsible for all browser automation: launching Chrome, opening
WhatsApp Web, finding a contact, and sending the message.

This is the only module that should import selenium — keeping browser
concerns isolated here means birthday_checker.py and main.py stay easy
to read and test without needing a real browser.
"""

import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import config
class WhatsAppSender:
    def __init__(self):
        self.driver = None
    def start(self):
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={config.CHROME_PROFILE_DIR}")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(config.WHATSAPP_URL)
        WebDriverWait(self.driver, config.QR_LOGIN_TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, '//div[@id="pane-side"]'))
        )
    def send_message(self, phone_number, message):
        url = f"{config.WHATSAPP_URL}/send?phone={phone_number}"
        self.driver.get(url)
        message_box = WebDriverWait(self.driver, config.SEARCH_TIMEOUT).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            )
        )
        time.sleep(config.MESSAGE_SEND_DELAY)
        pyperclip.copy(message)
        message_box.click()
        message_box.send_keys(Keys.CONTROL, "v")
        time.sleep(1)
        message_box.send_keys(Keys.ENTER)
        time.sleep(1)
        return True
    def stop(self):
        if self.driver:
            self.driver.quit()
            
if __name__ == "__main__":
    sender = WhatsAppSender()
    print("Opening WhatsApp Web... Scan QR code if first time!")
    sender.start()
    print("Login successful! Chat list detected!")
    time.sleep(5)
    sender.stop()
    print("Browser closed safely!")