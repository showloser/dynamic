from pyvirtualdisplay.display import Display
from os import path
import hashlib
import time

from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from selenium.common.exceptions import TimeoutException
import logging
import json



def setup_logger(log_file):
    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.ERROR)

    # Create a file handler and set the log level
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.CRITICAL)

    # Create a formatter and add it to the handlers
    log_format = '%(message)s'
    formatter = logging.Formatter(log_format)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)

    return logger

logger = setup_logger('PENETRATION_LOG.txt')

def payload_logging(outcome, source, extension_id, extension_name, url_of_website, payload_type, payload, time_of_injection, time_of_alert, payload_filename, packet_info):
    # Convert sets to lists
    payload = str(payload)
    packet_info = str(packet_info)

    payload_log = {
        "outcome": outcome,
        "source": source,
        "extensionId": extension_id,
        "extensionName": extension_name,
        "Url": url_of_website,
        "payloadType": payload_type,
        "payload": payload,
        "timeOfInjection": time_of_injection,
        "timeOfAlert": time_of_alert,
        "payload_fileName": payload_filename,
        "packetInfo": packet_info
    }

    log_message = json.dumps(payload_log)
    logger.critical(log_message)


def initialize(path_to_extension):
    with Display() as disp:
        print('true')
        # obtain relevant extension information'
        def get_ext_id(path_to_extension):
            abs_path = path.abspath(path_to_extension)
            m = hashlib.sha256()
            m.update(abs_path.encode("utf-8"))
            ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
            url_path = f"chrome-extension://{ext_id}/popup.html"
            return url_path, abs_path, ext_id
        
        def payloads(path_to_payload):
            payload_array = []
            try:
                with open(path_to_payload, 'r') as file:
                    # Read the contents of the file
                    for line in file:
                        payload = line.rstrip('\n')
                        payload_array.append(payload)
            except FileNotFoundError:
                print("File not found.")
            except IOError:
                print("An error occurred while reading the file.")
            
            return payload_array

        url_path, abs_path, ext_id = get_ext_id(path_to_extension)
        payloads = payloads('payloads/extra_small_payload.txt')

        options = ChromeOptions()
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        load_ext_arg = "load-extension=" + abs_path
        options.add_argument(load_ext_arg)
        driver = Chrome(service=Service(), options=options)


        window_name_new(driver, ext_id, url_path, payloads)

def window_name_new(driver, ext_id, url_path, payloads):
    source = 'window.name'
    ext_id = ext_id
    url_of_injection_example = 'https://www.example.com'
    url_of_injection_extension = url_path
    payload_file = 'small_payload.txt'

    try:
        # Navigate to example.com
        driver.get('https://www.example.com')
        example = driver.current_window_handle

        # Wait up to 5 seconds for the title to become "Example Domain"
        title_condition = EC.title_is('Example Domain')
        WebDriverWait(driver, 5).until(title_condition)

        # get page source code of example.com
        example_source_code = driver.page_source

        # get extension popup.html
        driver.switch_to.new_window('tab')
        driver.get(url_path)
        extension = driver.current_window_handle

        # get page source code of extension
        extension_source_code = driver.page_source


        for payload in payloads:
            # since window.name is obtained from the website url, we will inject javascript to change the window.name
            driver.switch_to.window(example)

            try:
                driver.execute_script(f'window.name = `{payload}`;')

                # get time of injection
                time_of_injection = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")

            except Exception as e:
                print(' !!!! PAYLOAD FAILLED !!!!')
                print('Error: ', str(e))
                continue

            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('[example] + Alert Detected +')

                # get time of success [1) example]
                time_of_success = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
                payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')
            
            except TimeoutException:
                print('[example] = No alerts detected =')
                payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')

                

            driver.switch_to.window(extension)
            driver.refresh()


            # check for alerts in extensions
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()

                print('[extension] + Alert Detected +')

                # get time of success [2) extension]
                time_of_success = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
                payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_extension, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')

            except TimeoutException:
                print('[extension] = No alerts detected =')
                payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_extension, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')


            driver.switch_to.window(example)

            # check for alerts in example
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('[example] + Alert Detected +')

                # get time of success [1) example]
                time_of_success = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")
                payload_logging("SUCCESS", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, time_of_success, payload_file, 'nil')
            except TimeoutException:
                print('[example] = No alerts detected =')

                payload_logging("FAILURE", source, ext_id, 'h1-replacer(v3)', url_of_injection_example, 'normal', payload, time_of_injection, 'nil', payload_file, 'nil')

            try: 
                # check modifications for example.com
                driver.switch_to.window(example)
                if example_source_code != driver.page_source:
                    driver.get("https://www.example.com")
                    print("Navigated back to 'https://www.example.com' due to page source changes")

            except:
                print('error')

            try: 
                # check modifications for extension
                driver.switch_to.window(extension)
                if extension_source_code != driver.page_source:
                    driver.get(url_path)
                    print(f"Navigated back to '{url_path}' due to extension page source changes")

            except:
                print('error')

    except TimeoutException:
        # Handle TimeoutException when title condition is not met
        print("Timeout: Title was not resolved to 'Example Domain'")

    except Exception as e:
        # Handle any other exceptions that occur
        print("An error occurred:", str(e))






# MAIN
initialize('Extensions/h1-replacer/h1-replacer(v3)_window.name')
