from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoAlertPresentException

from os import path
import hashlib

from pathlib import Path
import time

def initialize(path_to_extension):
    # obtain relevant extension information'
    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path
    
    def payloads(path_to_payload):
        payload_array = []
        try:
            with open(path_to_payload, 'r') as file:
                # Read the contents of the file
                for line in file:
                    payload_array.append(line)
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("An error occurred while reading the file.")
        
        return payload_array

    url_path, abs_path = get_ext_id(path_to_extension)
    payloads = payloads('payloads/small_payload.txt')

    # initialize selenium and load extension
    options = webdriver.ChromeOptions()
    options.add_experimental_option('detach', True)
    load_ext_arg = "load-extension=" + abs_path
    options.add_argument(load_ext_arg)
    options.add_argument("--enable-logging")
    driver = webdriver.Chrome('./chromedriver', options=options)




    # case 1:
    # window_name(driver, abs_path, url_path, payloads)

    # case 2:
    # location_href(driver, abs_path, url_path, payloads)


    # case 3:
    context_menu(driver, abs_path, url_path, payloads)

    # test(driver, abs_path, url_path, payloads)

################
# Case Scenario#
################

# 1) Window_name Entry Point
def window_name(driver, abs_path, url_path, payloads):

    # get www.example.com
    driver.get('https://www.example.com')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)


    for payload in payloads:
        # since window.name is obtained from the website url, we will inject javascript to change the window.name
        driver.switch_to.window(extension)
        driver.refresh()
        driver.switch_to.window(example)

        print(payload)

        driver.execute_script(f'window.name = `{payload}`;')

        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')



# 2) Location_href
def location_href(driver, abs_path, url_path, payloads):
    # get www.example.com
    driver.get('https://www.example.com')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)

    for payload in payloads:
        # we can inject a script to change the location.href variable using query parameters
        driver.switch_to.window(extension)
        driver.refresh()
        driver.switch_to.window(example)


        try:
            # driver.execute_script(f"location.href = 'https://www.example.com/?p'{payload}")
            driver.execute_script(f"location.href = 'https://www.example.com/?p'{payload}")

            time.sleep(1)
            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')

        except:
            print('Payload failed')



# 3) Context_Menu
def context_menu(driver, abs_path, url_path, payloads):
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.by import By
    from pynput.keyboard import Controller, Key


    # get www.example.com
    driver.get('file:///home/showloser/localhost/dynamic/miscellaneous/xss_website.html')
    # set handler for example.com
    example = driver.current_window_handle

    # get extension popup.html
    driver.switch_to.new_window('tab')
    extension = driver.current_window_handle
    driver.get(url_path)

    for payload in payloads:
        driver.switch_to.window(example)
        driver.execute_script(f'document.getElementById("h1_element").innerText = `{payload}`')

        target_element = driver.find_element(By.ID, 'h1_element')

        # Select the text using JavaScript
        driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)

        # perform right click to open context menu
        actions = ActionChains(driver)
        actions.context_click(target_element).perform()

        # navigate to extension context menu option
        keyboard = Controller()
        for _ in range(6):  
            # Press the arrow key down
            keyboard.press(Key.down)
            # Release the arrow key
            keyboard.release(Key.down)

        # Press the Enter key
        keyboard.press(Key.enter)
        # Release the Enter key
        keyboard.release(Key.enter)


        try:
            # wait 2 seconds to see if alert is detected
            WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print('+ Alert Detected +')
        except TimeoutException:
            print('= No alerts detected =')

    time.sleep(2)


# 4) onConnect (Hvt do)
def onConnect(driver,abs_path, url_path, paylaods):
    print('in progress')
    payload = '''
    const extId = "lghkoafcpkdkfgmdfobfcdcgeijohgnj";
    const port = chrome.runtime.connect(extId, { name: "content-script" });
    port.postMessage({ action: "activateExtension" });
    '''



def button_input_paradox():
    from bs4 import BeautifulSoup
    def hierarchy_method():
        # basically tries to associate which button is for the input by using the hierarchy as a guide (same parent)

        id_of_button = 'replaceButton'
        id_of_input = 'replacementInput'
        id_of_fakeButton = 'fakeButton'


        buttons = [id_of_button,id_of_fakeButton]
        buttons = [id_of_fakeButton,id_of_button]

        # input = [id_of_input]

        def find_associated_button(input, buttons, html_source):

            # Locate the input field using BeautifulSoup
            soup = BeautifulSoup(html_source, 'html.parser')
        
            for button_id in buttons:
                button = soup.find('button', id=button_id)
                if has_common_parent(input, button_id, html_source):
                    button_id = button.get('id')
                    return button_id
                
            # No associated button found
            return None

        def has_common_parent(input_field, button, html_source):
            soup = BeautifulSoup(html_source, 'html.parser')
            input_element = soup.find(id=input_field)
            button_element = soup.find(id=button)

            if (input_element.parent == button_element.parent):
                return True
            
            return False


        with open('Extensions/h1-replacer/h1-replacer_testing/popup.html', 'r') as file:
            html_source = file.read()

    
        associated_button_id = find_associated_button(id_of_input, buttons, html_source)
        print(associated_button_id)

    def button_proximity():
        # basically tries to associate which button is for the input by finding the nearest button to the input

        # Assuming 'html_source_code' contains the HTML source code
        with open('Extensions/h1-replacer/h1-replacer_testing/popup.html', 'r') as file:
            html_source = file.read()
        soup = BeautifulSoup(html_source, 'html.parser')

        # Assuming 'input_field_id' contains the ID of the input field
        input_field = soup.find('input', id='replacementInput')

        # Assuming 'button1_id' and 'button2_id' contain the IDs of the two buttons
        button1 = soup.find('button', id='fakeButton')
        button2 = soup.find('button', id='replaceButton')

        # Get the position of the input field and each button in the HTML document
        input_field_position = input_field.sourceline
        button1_position = button1.sourceline
        button2_position = button2.sourceline

        # Calculate the distance between the input field and each button based on their positions
        distance_button1 = abs(button1_position - input_field_position)
        distance_button2 = abs(button2_position - input_field_position)

        # Determine the nearest button
        nearest_button = button1 if distance_button1 < distance_button2 else button2

        # Print the ID of the nearest button
        print("Nearest Button:", nearest_button['id'])

    def prefix_comparison():
        # basically tries to associate which button is for which input by finding similarity in id names

        # Assuming 'html_source_code' contains the HTML source code
        with open('Extensions/h1-replacer/h1-replacer_testing/popup.html', 'r') as file:
            html_source = file.read()
        soup = BeautifulSoup(html_source, 'html.parser')

        input_id = "replacementInput" 
        button_ids = ["replaceButton", "fakeButton"]
        button_ids = ["fakeButton", "replaceButton"]

        # Create a dictionary to store the common prefix lengths for each button
        common_prefix_lengths = {}



        # Compare the prefix of input ID with the button IDs
        for button_id in button_ids:
            # Find the common prefix between the input ID and button ID
            common_prefix = ''
            for a, b in zip(input_id, button_id):
                if a != b:
                    break
                common_prefix += a

            # Store the length of the common prefix for each button
            common_prefix_lengths[button_id] = len(common_prefix)

        # Find the button ID with the highest common prefix length
        button_with_highest_prefix = max(common_prefix_lengths, key=common_prefix_lengths.get)
        print("button_with_highest_prefix: " + button_with_highest_prefix)


        # # [Verbose mode]#

        # # Sort the button IDs based on the common prefix length in descending order
        # sorted_button_ids = sorted(common_prefix_lengths, key=common_prefix_lengths.get, reverse=True)

        # # Print the sorted button IDs along with their common prefix lengths (rankings)
        # for rank, button_id in enumerate(sorted_button_ids, start=1):
        #     common_prefix_length = common_prefix_lengths[button_id]
        #     print(f"Rank {rank}: Button ID {button_id} (Common Prefix Length: {common_prefix_length})")

        






# # Main Program #
# initialize('Extensions/h1-replacer/h1-replacer_button_paradox')


# initialize('Extensions/h1-replacer/h1-replacer(v3)_context_menu')









## HEADLESS CONTEXT_MENUS
def headless4ContextMenus():
    from pyvirtualdisplay.display import Display
    from os import path
    import hashlib
    import time

    from selenium.webdriver.common.by import By
    from selenium.webdriver import ActionChains, Chrome, ChromeOptions, Keys
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver import Chrome, ChromeOptions
    from selenium.webdriver.chrome.service import Service

    import subprocess

    def payloads(path_to_payload):
        payload_array = []
        try:
            with open(path_to_payload, 'r') as file:
                # Read the contents of the file
                for line in file:
                    payload_array.append(line)
        except FileNotFoundError:
            print("File not found.")
        except IOError:
            print("An error occurred while reading the file.")

        return payload_array

    def get_ext_id(path_to_extension):
        abs_path = path.abspath(path_to_extension)
        m = hashlib.sha256()
        m.update(abs_path.encode("utf-8"))
        ext_id = "".join([chr(int(i, base=16) + 97) for i in m.hexdigest()][:32])
        url_path = f"chrome-extension://{ext_id}/popup.html"
        return url_path, abs_path
        



    with Display() as disp:

        payloads = payloads('payloads/small_payload.txt')
        url_path, abs_path = get_ext_id('Extensions/h1-replacer/h1-replacer(v3)_context_menu')

        print(disp.is_alive())
        print(disp.display)
        options = ChromeOptions()
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        load_ext_arg = "load-extension=" + abs_path
        options.add_argument(load_ext_arg)
        driver = Chrome(service=Service(), options=options)

        # get www.example.com
        driver.get('file:///home/showloser/localhost/dynamic/miscellaneous/xss_website.html')
        # set handler for example.com
        example = driver.current_window_handle

        # get extension popup.html
        driver.switch_to.new_window('tab')
        extension = driver.current_window_handle
        driver.get(url_path)
        driver.save_screenshot('ss.png')
        time.sleep(2)

        for payload in payloads:
            print(payload)
            # driver.switch_to.window(extension)
            # driver.refresh()

            driver.switch_to.window(example)

            driver.execute_script(f'document.getElementById("h1_element").innerText = `{payload}`')
            target_element = driver.find_element(By.ID, 'h1_element')

            # Select the text using JavaScript
            driver.execute_script("window.getSelection().selectAllChildren(arguments[0]);", target_element)


            actions = ActionChains(driver)
            actions.context_click(target_element).perform()


            driver.save_screenshot('ss.png')
            time.sleep(2)


            for _ in range(6):
                subprocess.call(['xdotool', 'key', 'Down'])

            # Simulate pressing the "Enter" key
            subprocess.call(['xdotool', 'key', 'Return'])

            try:
                # wait 2 seconds to see if alert is detected
                WebDriverWait(driver, 2).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print('+ Alert Detected +')
            except TimeoutException:
                print('= No alerts detected =')


            driver.switch_to.window(extension)
            driver.save_screenshot('ss.png')
            time.sleep(1)


            driver.switch_to.window(example)
            driver.save_screenshot('ss.png')
            time.sleep(1)
            




