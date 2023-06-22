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
from multiprocessing import Pool
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.chrome.service import Service





def get_ext_id(path_to_extension):
    abs_path = path.abspath(path_to_extension)
    m = hashlib.sha256()
    m.update(abs_path.encode("utf-8"))
    ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
    url_path = f"chrome-extension://{ext_id}/popup.html"
    return url_path, abs_path

url_path, abs_path = get_ext_id('Extensions/h1-replacer/h1-replacer_testing')

def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)


    driver.get(url_path)
    original = driver.current_window_handle
    driver.switch_to.new_window('tab')
    new = driver.current_window_handle

    driver.get('https://www.example.com')
    driver.switch_to.window(original)

    # a = driver.find_element(By.ID, 'replacementInput')
    # a.clear()
    # a.send_keys('caoni ma')
    # button = driver.find_element(By.ID, 'replaceButton')
    # button.click()


    # driver.execute_script('document.getElementById("replacementInput").value = "<img src=x onerror=alert(1)>"')


    driver.execute_script('document.getElementById("replacementInput").value = "<img src=x onerror=document.write(1)>"')


    driver.execute_script('document.getElementById("replaceButton").click()')   

    driver.switch_to.window(new)




main()




# def baseline():
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option('detach', True)
#     load_ext_arg = "load-extension=" + abs_path
#     options.add_argument(load_ext_arg)
#     options.add_argument("--enable-logging")
#     driver = webdriver.Chrome('./chromedriver', options=options)

#     driver.get(url_path)
#     clickable_elements = driver.find_elements_by_xpath("//a|//button")
#     for element in clickable_elements:
#         element.click()



