from functools import partial
from urllib.parse import quote_plus

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.chat_gpt import ask_chat_gpt
from lens_gpt_backend.utils.driver_pool import driver_pool
from lens_gpt_backend.utils.product import Product
from lens_gpt_backend.utils.utils import distinct

ASSISTANT_INSTR = ("You are an helpful assistant which helps me to find the website of the original producer "
                   "of a specific product. I have the urls of multiple websites which showed up when I searched "
                   "for that product. They are enumerated. Please give me the number of the website which "
                   "is most likely the original producer of the product. It is very important that you only return "
                   "the number of the website and not any other information.")

EXAMPLE_TITLES = ("Product: Patagonia Fitz Roy Trout Trucker Hat\n"
                  "1. https://eu.patagonia.com/de/de/product/fitz-roy-trout-trucker-hat/38288.html\n"
                  "2. https://zefixflyfishing.com/products/patagonia-fitz-roy-trout-trucker-hat\n"
                  "3. https://www.rudiheger.eu/fitz-roy-trout-trucker-hat-black.html\n"
                  "4. https://www.adh-fishing.de/bekleidung/kopfbedeckungen/kappen-und-huete/patagonia-fitz-roy-trout-trucker-hat-kappe-witn")

EXAMPLE_ANSWERS = "1"


class ProducerWebsite(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        base_url = "https://google.com/"
        search_dict = input_value.get_dict_str_str()
        search_term = f"{search_dict['producer']} {search_dict['model']}"
        scape_function = partial(_get_urls_for_image, search_term)
        result = driver_pool.execute(scape_function, base_url)
        return result, True


def build_google_search_url(query: str) -> str:
    base_url = "https://www.google.com/search?q="
    encoded_query = quote_plus(query)
    return base_url + encoded_query


def _get_urls_for_image(search: str, driver: WebDriver, wait: WebDriverWait[WebDriver]) -> Product:
    search_format = build_google_search_url(search)
    driver.get(search_format)

    # Get all links from the search by getting all a tags from the center column with id center_col
    links = driver.find_elements(By.CSS_SELECTOR, "#res a")
    urls = [link.get_attribute("href") for link in links]
    non_google_urls = distinct([url for url in urls if url and "google.com" not in url])
    enumerate_urls = [f"{i + 1}. {url}" for i, url in enumerate(non_google_urls)]
    input_urls = "\n".join(enumerate_urls[:7])
    prompt = f"Product: {search}\n{input_urls}"
    response = ask_chat_gpt(ASSISTANT_INSTR, [EXAMPLE_TITLES, EXAMPLE_ANSWERS, prompt])

    if response:
        return Product(non_google_urls[int(response) - 1], data_description="url")

    raise ValueError("No response from AI model!")
