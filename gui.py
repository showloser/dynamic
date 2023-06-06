import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from os import path
import hashlib

def gui():
    # getting id of extension [start]
    def get_ext_id():
        abs_path = path.abspath("Extensions/h1-replacer/h1-replacer")
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path


    options = webdriver.ChromeOptions()
    # prevent chrome browser from closing and define extension
    options.add_experimental_option('detach', True)
    options.add_argument('--load-extension=Extensions/h1-replacer/h1-replacer')
    
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)

    # open chrome extension in browser
    url_path = get_ext_id()
    driver.get(url_path)

    # Use extension in context of www.example.com
    original = driver.current_window_handle
    driver.switch_to.new_window('tab')
    new = driver.current_window_handle
    driver.get('https://www.example.com')
    driver.get_screenshot_as_file("ss.png")


    # switch back to extension context
    driver.switch_to.window(original)
    entry_point = driver.find_element(By.ID,'replacementInput')
    payload = '<img src=x onerror="alert("1")">'

    entry_point.send_keys(payload)
    driver.get_screenshot_as_file("ss.png")


gui()