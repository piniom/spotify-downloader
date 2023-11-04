import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time

def get_driver(download_directory: str) -> webdriver.Firefox:
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", download_directory)

    options = Options()
    options.profile = profile
    options.add_argument("--headless")

    return webdriver.Firefox(options=options)

def find_element(driver: webdriver.Firefox, tag: str, inner_text: str):
    elements = driver.find_elements(by=By.TAG_NAME, value=tag)
    return next(filter(lambda b: b.text == inner_text, elements))

def find_button(driver: webdriver.Firefox, inner_text: str):
    return find_element(driver, 'button', inner_text)

def find_link(driver: webdriver.Firefox, inner_text: str):
    return find_element(driver, 'a', inner_text)

def wait_for_link(driver: webdriver.Firefox, inner_text: str):
    t = 0.05
    while True:
        try:
            return find_link(driver, inner_text)
        except:
            t *= 2
            t = min(1, t)
            time.sleep(t)

def wait_for_download_list(driver: webdriver.Firefox):
    t = 0.05
    while len(driver.find_elements(by=By.TAG_NAME, value='input')) != 0:
        t *= 2
        t = min(1, t)
        time.sleep(t)

def sanitize_filename(filename):
    illegal_characters = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in illegal_characters:
        filename = filename.replace(char, '')
    return filename

def check_file_exists(directory: str, file: str):
    for filename in os.listdir(directory):
        if os.path.splitext(file)[0] in os.path.splitext(filename)[0]:
            return True  
    return False

def wait_file_exists(directory: str, filename: str):
    t = 0.05
    while not check_file_exists(directory, filename):
        t *= 2
        t = min(1, t)
        time.sleep(t)