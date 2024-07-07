from functools import partial

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.driver_pool import driver_pool
from lens_gpt_backend.utils.product import Product

LENS_ICON_CSS = ("body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form >"
                 " div:nth-child(1) > div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.nDcEnd")
ITEM_CSS = "GZrdsf.oYxtQd.lXbkTc"


def _get_item_urls(element: WebElement) -> dict[str, str | None]:
    url = element.get_attribute("href")
    title = element.find_element(By.CSS_SELECTOR, "div:nth-child(1)").get_attribute("data-item-title")
    img = element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
    return {"url": url, "title": title, "img": img}


def _get_urls_for_image(image_path: str, driver: WebDriver, wait: WebDriverWait[WebDriver]) -> Product:
    driver.get("https://www.google.com/")

    # Click on lens icon
    driver.find_element(By.CSS_SELECTOR, LENS_ICON_CSS).click()

    # Wait for the upload button to be visible and interact with it
    upload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    upload.send_keys(image_path)

    try:
        urls_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, ITEM_CSS)))
        elements = []
        for element in urls_elements:
            try:
                elements.append(_get_item_urls(element))
            except NoSuchElementException as e:
                print(e)
        return Product(elements, data_description="item-urls")  # type: ignore
    except NoSuchElementException as e:
        print(e)
        return Product([], data_description="item-urls")


class LensLinksProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        base_url = "https://google.com/"
        scape_function = partial(_get_urls_for_image, input_value.get_str())
        result = driver_pool.execute(scape_function, base_url)
        return result, True
