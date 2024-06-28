import os
import threading
from dataclasses import dataclass
from queue import Queue
from typing import Callable, TypeVar

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from lens_gpt_backend.utils.accept_cookies import _google_accept_cookies

R = TypeVar('R')

ACCEPT_COOKIE_FUNCTIONS = {
    "https://google.com/": _google_accept_cookies
}


@dataclass
class DriverWrapper:
    def __init__(self, driver: WebDriver, wait: WebDriverWait[WebDriver], cookies: dict[str, bool]):
        self.driver = driver
        self.wait = wait
        self.cookies = cookies


def _init_new_driver() -> DriverWrapper:
    options = webdriver.ChromeOptions()
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Check if running in Docker by looking for the .dockerenv file
    if os.path.exists('/.dockerenv'):
        options.add_argument('--headless')
        service = Service(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(options=options, service=service)
    else:
        driver = webdriver.Chrome(options=options)

    wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
    return DriverWrapper(driver, wait, {})


class DriverPool:
    def __init__(self, max_drivers: int):
        self.max_drivers = max_drivers
        self.driver_queue = Queue[DriverWrapper]()
        self.lock = threading.Lock()
        self.active_drivers = 0

    def execute(self, function: Callable[[WebDriver, WebDriverWait[WebDriver]], R], base_url: str) -> R:
        driver_wrapper = self._get_driver()

        if base_url not in driver_wrapper.cookies:
            ACCEPT_COOKIE_FUNCTIONS[base_url](driver_wrapper.driver)
            driver_wrapper.cookies[base_url] = True

        try:
            return function(driver_wrapper.driver, driver_wrapper.wait)
        finally:
            self._release_driver(driver_wrapper)

    def _get_driver(self) -> DriverWrapper:

        with self.lock:
            if self.driver_queue.empty() and self.active_drivers < self.max_drivers:
                wrapper = _init_new_driver()
                self.active_drivers += 1
            else:
                wrapper = self.driver_queue.get()

        return wrapper

    def _release_driver(self, driver: DriverWrapper) -> None:
        with self.lock:
            self.driver_queue.put(driver)


driver_pool = DriverPool(max_drivers=5)
