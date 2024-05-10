
import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()


def get_urls_for_image(image_path: str) -> list[dict[str, str]]:
    _accept_cookies(driver)
    driver.get("https://www.google.com/")

    # Click on lens icon
    driver.find_element(By.CSS_SELECTOR, "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > "
                                         "div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.nDcEnd").click()

    # Wait for the upload button to be visible
    driver.implicitly_wait(1)
    upload = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    upload.send_keys(image_path)
    sleep(4)

    # Find all urls, the a tags have the class "GZrdsf oYxtQd lXbkTc"
    try:
        urls = driver.find_elements(By.CLASS_NAME, "GZrdsf.oYxtQd.lXbkTc")
        return [_get_item_urls(url) for url in urls]
    except Exception as e:
        print(e)
        return []


def _get_item_urls(element):
    url = element.get_attribute("href")
    title = element.find_element(By.CSS_SELECTOR, "div:nth-child(1)").get_attribute("data-item-title")
    img = element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    return {"url": url, "title": title, "img": img}


def _accept_cookies(driver):
    try:
        driver.get("https://www.google.com/")
        driver.find_element(By.ID, "L2AGLb").click()
    except Exception as e:
        print(e)
