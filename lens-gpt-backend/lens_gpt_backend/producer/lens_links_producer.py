from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from lens_gpt_backend.producer.producer import Producer


class LensLinksProducer(Producer[str, dict[str, str]]):

    def produce(self, image_path: str) -> tuple[list[dict[str, str]], bool]:
        urls = self._get_urls_for_image(image_path)
        return urls, False

    def _get_urls_for_image(self, image_path: str, driver: WebDriver, wait: WebDriverWait[WebDriver]) -> list[dict[str, str]]:

        driver.get("https://www.google.com/")

        # Click on lens icon
        driver.find_element(By.CSS_SELECTOR, "body > div.L3eUgb > div.o3j99.ikrT4e.om7nvf > form > div:nth-child(1) > "
                                             "div.A8SBwf > div.RNNXgb > div > div.dRYYxd > div.nDcEnd").click()

        # Wait for the upload button to be visible and interact with it
        upload = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
        upload.send_keys(image_path)

        try:
            urls_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "GZrdsf.oYxtQd.lXbkTc")))
            return [self._get_item_urls(element) for element in urls_elements]
        except Exception as e:
            print(e)
            return []

    def _get_item_urls(self, element):
        url = element.get_attribute("href")
        title = element.find_element(By.CSS_SELECTOR, "div:nth-child(1)").get_attribute("data-item-title")
        img = element.find_element(By.CSS_SELECTOR, "img").get_attribute("src")
        return {"url": url, "title": title, "img": img}
