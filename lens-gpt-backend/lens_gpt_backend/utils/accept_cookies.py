from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By


def _google_accept_cookies(driver: WebDriver) -> None:
    driver.get("https://www.google.com/")
    driver.find_element(By.ID, "L2AGLb").click()
