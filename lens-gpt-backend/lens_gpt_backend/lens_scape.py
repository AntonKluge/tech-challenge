
import os
from time import sleep

from diskcache import Cache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')


# Use the specific version of ChromeDriver that matches your ChromeDriver version
driver = webdriver.Chrome(options=options)

wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
COOKIES_ACCEPTED = False


def get_urls_for_image(image_path: str) -> list[dict[str, str]]:
    _accept_cookies()
    driver.get("https://www.google.com/")

    # Click on lens icon
    driver.find_element(By.CSS_SELECTOR, "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > "
                                         "div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.nDcEnd").click()

    # Wait for the upload button to be visible and interact with it
    upload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    upload.send_keys(image_path)

    try:
        urls_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "GZrdsf.oYxtQd.lXbkTc")))
        return [_get_item_urls(element) for element in urls_elements]
    except Exception as e:
        print(e)
        return []


def _get_item_urls(element):
    url = element.get_attribute("href")
    title = element.find_element(By.CSS_SELECTOR, "div:nth-child(1)").get_attribute("data-item-title")
    img = element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    return {"url": url, "title": title, "img": img}


def _accept_cookies():
    global COOKIES_ACCEPTED
    if COOKIES_ACCEPTED:
        return

    try:
        driver.get("https://www.google.com/")
        driver.find_element(By.ID, "L2AGLb").click()
        COOKIES_ACCEPTED = True
    except Exception as e:
        print(e)
