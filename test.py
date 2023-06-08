import time
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.common.by import By
from os import path
import hashlib
from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay.display import Display
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
import logging
from multiprocessing import Pool
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC




def logs(driver, alert, result, extension_name, payload):
    # !! [Selenium cant take screenshot of alerts as it occurs outside the DOM] !!
    # driver.save_screenshot("alert_screenshot.png")
    try:
        # Log the info (both success and fail)
        if result == 'Success':
            alert_text = alert.text
            alert.accept()  # Accept the alert window
            logging.critical(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {result}, {logging.getLevelName(logging.CRITICAL)}, {extension_name}, {alert_text}, {payload}")
        else:
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, {result}, {logging.getLevelName(logging.info)}, {extension_name}, 'NIL', {payload}")
    except NoAlertPresentException:
        logging.warning("No alert present")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


def process_payload(payloads):
    
    # Getting id of extension [start]
    url_path = 'chrome-extension://hhjaeikcadjhmdnehfpblhbcfijkdmdp/popup.html'
    abs_path = '/home/showloser/localhost/dynamic/Extensions/h1-replacer/h1-replacer'

    options = ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)


    driver = Chrome(service=Service(), options=options)
    driver.get(url_path)
    original = driver.current_window_handle
    driver.switch_to.new_window('tab')
    new = driver.current_window_handle

    driver.get('https://www.example.com')
    driver.switch_to.window(original)
    
    time.sleep(1)
    driver.get_screenshot_as_file('ss.png')

    a = driver.find_element(By.ID, 'replacementInput')
    a.clear()

    # payload = '<img src=xss onerror=alert(1)>'
    # payload= '<img src=xss onerror=document.write("qwer$#@!")>'
    payload = 'test123'

    a.send_keys(payload)
    button = driver.find_element(By.ID, 'replaceButton')
    button.click()
    
    time.sleep(1)
    driver.get_screenshot_as_file('ss.png')

    driver.switch_to.window(new)

    time.sleep(1)
    driver.get_screenshot_as_file('ss.png')





















def headless(extension_path):
    # Getting id of extension [start]
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path

    url_path, abs_path = get_ext_id(extension_path)
    print(url_path)
    print(abs_path)

    # def subset_payloads(file_path):
    #     payloads1 = []
    #     payloads2 = []
    #     payloads3 = []

    #     with open(file_path, 'r') as file:
    #         for line in file:
    #             payload = line.strip()  # Remove leading/trailing whitespace
    #             # Assign the payload to one of the subsets
    #             if len(payloads1) < len(payloads2) and len(payloads1) < len(payloads3):
    #                 payloads1.append(payload)
    #             elif len(payloads2) < len(payloads3):
    #                 payloads2.append(payload)
    #             else:
    #                 payloads3.append(payload)

    #     return payloads1, payloads2, payloads3

    # payloads1, payloads2, payloads3 = subset_payloads('payloads/small_payload.txt')

    # num_processes = 3  # Define the number of concurrent processes
    # with Pool(num_processes) as pool:
    #     pool.map(process_payload, [payloads1, payloads2, payloads3])

    process_payload([])


def main():
    # Configure logging
    logging.basicConfig(
        filename='logs/penetration_log_headless.txt',
        level=logging.ERROR,
        format='%(asctime)s, %(message)s'
    )

    # Run program
    with Display() as disp:
        print(disp.is_alive())
        headless('Extensions/h1-replacer/h1-replacer')



if __name__ == '__main__':
    main()



