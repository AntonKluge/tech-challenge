from functools import partial
import re

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.driver_pool import driver_pool, format_url_parameter
from lens_gpt_backend.utils.product import Product

_URL = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw={search}&_sacat=0&_ipg=240"


class SecondHandOfferProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        search_function = partial(_get_second_hand_offers, input_value.get_dict_str_str())
        result = driver_pool.execute(search_function, "https://ebay.com/")

        return result  # type: ignore


def _get_second_hand_offers(search: dict[str, str], driver: WebDriver, wait: WebDriverWait[WebDriver]) -> Product:
    search_term = search["producer"] + " " + search["model"]
    search_url = _URL.format(search=format_url_parameter(search_term))
    driver.get(search_url)

    # Get all li who's id starts with "item"
    items = driver.find_elements(By.XPATH, "//li[starts-with(@id, 'item')]")
    items_parsed = [_extract_item(item) for item in items]

    return Product(items_parsed, data_description="second-hand-offers"), True  # type: ignore


def _extract_item(element: WebElement) -> dict[str, str | float]:
    # Extract link - a tag with s-item__link class
    link = element.find_element(By.CLASS_NAME, "s-item__link").get_attribute("href")

    # State - span tag with SECONDARY_INFO class
    state = element.find_element(By.CLASS_NAME, "SECONDARY_INFO").text

    # Price - span tag with s-item__price class
    price = element.find_element(By.CLASS_NAME, "s-item__price").text
    price_euro = _do_price_conversion_to_euro(price)

    return {"link": link if link else "", "state": state, "price": price_euro}


def _do_price_conversion_to_euro(price: str) -> float:
    if '$' in price:
        price = price.replace('$', '')
        return _get_first_price(price) * 0.9239
    if '€' in price:
        price = price.replace('€', '')
        return _get_first_price(price)

    # extract the number from the string
    return _get_first_price(price)


def _get_first_price(price: str) -> float:
    # Use regex to find the first occurrence of a pattern that represents a price (digits followed by a dot followed by digits)
    match = re.search(r"\d+\.\d+", price)
    if match:
        return float(match.group())

    raise ValueError("No price found in the string")

