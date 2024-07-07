from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def _google_accept_cookies(driver: WebDriver) -> None:
    driver.get("https://www.google.com/")
    driver.find_element(By.ID, "L2AGLb").click()


def _ebay_accept_cookies(driver: WebDriver) -> None:
    driver.get("https://www.ebay.com/")
    wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
    accept_button = wait.until(EC.element_to_be_clickable((By.ID, "gdpr-banner-accept")))
    sleep(1)  # Wait for the button to be clickable
    accept_button.click()
