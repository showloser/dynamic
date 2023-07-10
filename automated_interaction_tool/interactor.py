import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from os import path
import hashlib

def find_all_interactable_elements(driver):
    interactable_elements = []

    # Find all interactable <a> tags, <button> elements, and <input> elements
    interactable_elements.extend(driver.find_elements(By.TAG_NAME, 'a'))
    interactable_elements.extend(driver.find_elements(By.TAG_NAME, 'button'))
    interactable_elements.extend(driver.find_elements(By.TAG_NAME, 'input'))
    
    # Find all interactable <input> elements with type="checkbox" or type="radio"
    interactable_elements.extend(driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]'))
    interactable_elements.extend(driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]'))
    
    # Find all interactable <select> elements
    interactable_elements.extend(driver.find_elements(By.TAG_NAME, 'select'))
    
    # Find all interactable <textarea> elements
    interactable_elements.extend(driver.find_elements(By.TAG_NAME, 'textarea'))
    
    return interactable_elements


def find_all_input_fields(driver):
    input_fields = []
    
    # Find all <input> elements
    input_fields.extend(driver.find_elements(By.TAG_NAME, 'input'))
    
    # Find all <textarea> elements
    input_fields.extend(driver.find_elements(By.TAG_NAME, 'textarea'))
    
    return input_fields



def main():

    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path

    url_path, abs_path = get_ext_id('automated_interaction_tool/h1-replacer_button_paradox')


    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)


    driver.get(url_path)

    # # find all interactable_elements
    # interactable_elements = find_all_interactable_elements(driver)
    # for element in interactable_elements:
    #     print(element.get_attribute("outerHTML"))

    # find all input fields
    input_fields = find_all_input_fields(driver)
    for field in input_fields:
        print(field.get_attribute("outerHTML"))



    # driver.quit()






main()




