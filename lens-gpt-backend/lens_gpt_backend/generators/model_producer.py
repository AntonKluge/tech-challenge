from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lens_gpt_backend.generators.generators import Generators

client = OpenAI(api_key="sk-proj-s7WyfYnogKGcT6Ty30DDT3BlbkFJmn11EtBLGWsK5jAgWjEW")

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument('--no-sandbox')  # Bypass OS security model
options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration

service = Service(executable_path="/usr/bin/chromedriver")

# Use the specific version of ChromeDriver that matches your ChromeDriver version
driver = webdriver.Chrome(options=options, service=service)

wait = WebDriverWait(driver, 10)  # Timeout after 10 seconds
COOKIES_ACCEPTED = False


class ModelProducer(Generators):

    def __init__(self, file_path: str):
        super().__init__("model_producer", file_path)

    def generate(self) -> tuple[dict[str, str], bool]:
        urls = _get_urls_for_image(self._file_path)
        model_producer = _get_producer_model(urls)
        return model_producer, True


def _get_urls_for_image(image_path: str) -> list[dict[str, str]]:
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


def _get_producer_model(items: list[dict[str, str]]) -> dict[str, str]:
    titles = [item['title'] for item in items if item['title']]
    input_text = "\n".join(titles)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an helpful assistant which helps me to identify clothing. I have the title of "
                           "multiple websites which sell that specific piece of clothing I am looking for. Please "
                           "extract the producer and model of the item based of the title of the websites I found. "
                           "Do not extract size information or other irrelevant details, just the model name!"
                           "If multiple producers or models were mentioned, return the one that is most mentioned "
                           "and makes the most sense. Answer in the pattern:"
                           "\n\nproducer: \"Producer\"\nmodel: \"Model\""
            },
            {
                "role": "user",
                "content": "Patagonia P-6 Logo Responsibili Long sleeve (black 2)\nPatagonia Bicycle T-Shirts for Men | "
                           "Mercari\nเสื้อpatagoniaแท้ ราคาพิเศษ | ซื้อออนไลน์ที่ Shopee ส่งฟรี*ทั่วไทย!\nPolera Manga "
                           "Larga Patagonia | MercadoLibre 📦\nNone\nNone\nMen’s size S Patagonia shirt. Never worn. - "
                           "Depop\nPatagonia | Shirts | Patagonia Long Sleeve Black T Shirt Mens Size S | "
                           "Poshmark\nPatagonia Loong Sleeve\nPositive.cnx | Patagonia Sz. อก 22' ยาว 28' สภาพใหม่ "
                           "ไม่มีตำหนิ สภาพ9/10 ♦️Soldout♦️ Dm:po... | Instagram\n1点限り❣️ Patagonia パタゴニア 長袖 Tシャツ トップス "
                           "ブラック 黒 L パタゴニア トップス - axiomaenergiasolar.com\n[美品]パタゴニア　patagonia ロンT 黒 by メルカリ\nPatagonia "
                           "Men's P-6 Logo Long-Sleeve Responsibili-Tee | Patagonia long sleeve, Tees, Patagonia"
            },
            {
                "role": "assistant",
                "content": "producer: Patagonia\nmodel: Patagonia Men's Long-Sleeved P-6 Logo Responsibili-Tee"
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Parse the response to extract the producer and model
    response_text = response.choices[0].message.content
    lines = response_text.strip().split("\n")
    producer = lines[0].split(": ")[1].strip('\"')
    model = lines[1].split(": ")[1].strip('\"')

    return {"producer": producer, "model": model}
