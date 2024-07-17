from functools import partial

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from shapely import Polygon
from shapely.geometry import box

from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.chat_gpt import ask_chat_gpt
from lens_gpt_backend.utils.driver_pool import driver_pool
from lens_gpt_backend.utils.product import Product

ASSISTANT_INSTRUCTION = ("You are a helpful assistant who helps me extract specific information for a piece of "
                         "clothing from a blob of text. I will give you an unsorted piece of text, where all the "
                         "information is in. I want you to extract the following information: Price, Original Name, "
                         "Description, Material, Specs. When returning them each should be in its own line, "
                         "followed by a : and then the information, e.g.\nPrice: 130.00.")

USER_PROMPT = ("Extract the information from the following blob:\n\nFleece Men's Better Sweater™ 1/4-Zip Fleece New "
               "Navy Model ist 1,85 m groß und trägt Größe Medium. Model ist 1,85 m groß und trägt Größe Medium. "
               "Model ist 1,96 m groß und trägt Größe X-Large. Model ist 1,96 m groß und trägt Größe X-Large. Model "
               "ist 1,96 m groß und trägt Größe X-Large. Model ist 1,96 m groß und trägt Größe X-Large. Men's Better "
               "Sweater™ 1/4-Zip Fleece Bewertung: 4.8 / 5 980 Rezensionen 130,00 € Farbe New Navy Sale Größe "
               "Größenleitfaden XS Warteliste S Warteliste M Warteliste L Warteliste XL Warteliste XXL Zum Warenkorb "
               "Versandinformation, Rücksendung & Umtausch Dieser warme 3/4 Zipper Pulli aus 100% Recycling-Polyester "
               "kombiniert den Look eines Strickpullovers mit der Pflegeleichtigkeit von Better Sweater Fleece. Der "
               "Stoff ist nach einem umweltfreundlichen Verfahren gefärbt, das den Wasser-, Energie- und "
               "Chemikalienbedarf gegenüber konventionellen Methoden reduziert. Hergestellt in einem Fair Trade "
               "Certified™-Betrieb. New Navy NENA | Modell-Nr. 25523 Passform Normaler Schnitt Was die Kunden sagen: "
               "Passt genau Alle Rezensionen ansehen Für mehr Informationen besuche unseren Größenleitfaden "
               "Spezifikationen & Features Strickoptik-Fleece aus 100% Recycling-Polyester Warmes, weiches und "
               "haltbares Fleece in Strickoptik aus 100% Recycling-Polyester, gefärbt nach einem umweltschonenden "
               "Verfahren, das den Wasser-, Energie- und Chemikalien-Bedarf gegenüber konventionellen Methoden "
               "reduziert Viertellanger Zipper und Stehkragen Viertellanger Zipper bis durch den Stehkragen mit einer "
               "Paspel-Schieberabdeckung Mit Raglanärmeln Raglanärmel für Mobilität und Komfort unter dem Rucksack "
               "Zipper-Brusttasche links Senkrechte Zipper-Brusttasche links für wichtige Dinge Hautfreundliche "
               "Abschlüsse an Saum und Bündchen Weiche, formbeständige und abriebfeste Besätze an Ärmeln und Saum "
               "Flachnaht-Konstruktion Konstruktion mit Flachnähten, die nicht auftragen oder scheuern Wir "
               "unterstützen die Menschen, die dieses Produkt herstellen Hergestellt in einem Fair Trade "
               "Certified™-Betrieb, d. h. dass die NäherInnen einen Zuschlag bekommen Herkunftsland Hergestellt in "
               "Thailand. Gewicht 505 g Materialien Hauptmaterial 339 g/m² Fleece aus 100% Recycling-Polyester; "
               "gefärbt nach einem umweltschonenden Verfahren, das den Wasser Energie- und Chemikalien-Bedarf "
               "gegenüber konventionellen Methoden reduziert Einfassungen Flauschiger 180 g/m² Trikot aus 100% "
               "Recycling-Polyester Die Einfassungen sind bluesign™-zertifiziert Hergestellt in einem Fair Trade "
               "Certified™-Betrieb Pflegehinweise Maschinenwäsche mit warmem Wasser, nicht bleichen, schonendes "
               "Schleudern, nicht bügeln Strickwaren neigen von Natur aus zu Knötchenbildung (Pilling) - auch dieses "
               "Modell. Das Entfernen der Knötchen trägt dazu bei, dass du deinen Patagonia Sweater länger tragen "
               "kannst. Und mit einem Sweater Stone geht das ganz einfach. Weitere Informationen zum Entfernen von "
               "Knötchen unter wornwear.com")

SYSTEM_ANSWER = ("Price: 130.00\nOriginal Name: Men's Better Sweater™ 1/4-Zip Fleece\nDescription: Dieser warme 3/4 "
                 "Zipper Pulli aus 100% Recycling-Polyester kombiniert den Look eines Strickpullovers mit der "
                 "Pflegeleichtigkeit von Better Sweater Fleece. Der Stoff ist nach einem umweltfreundlichen Verfahren "
                 "gefärbt, das den Wasser-, Energie- und Chemikalienbedarf gegenüber konventionellen Methoden "
                 "reduziert. Hergestellt in einem Fair Trade Certified™-Betrieb.\nMaterial: 100% "
                 "Recycling-Polyester\nSpecs: Strickoptik-Fleece aus 100% Recycling-Polyester Warmes, weiches und "
                 "haltbares Fleece in Strickoptik aus 100% Recycling-Polyester, gefärbt nach einem umweltschonenden "
                 "Verfahren, das den Wasser-, Energie- und Chemikalien-Bedarf gegenüber konventionellen Methoden "
                 "reduziert Viertellanger Zipper und Stehkragen Viertellanger Zipper bis durch den Stehkragen mit "
                 "einer Paspel-Schieberabdeckung Mit Raglanärmeln Raglanärmel für Mobilität und Komfort unter dem "
                 "Rucksack Zipper-Brusttasche links Senkrechte Zipper-Brusttasche links für wichtige Dinge "
                 "Hautfreundliche Abschlüsse an Saum und Bündchen Weiche, formbeständige und abriebfeste Besätze an "
                 "Ärmeln und Saum Flachnaht-Konstruktion Konstruktion mit Flachnähten, die nicht auftragen oder "
                 "scheuern Wir unterstützen die Menschen, die dieses Produkt herstellen Hergestellt in einem Fair "
                 "Trade Certified™-Betrieb, d. h. dass die NäherInnen einen Zuschlag bekommen")


class ModelInformationProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        producer_url = input_value.get_dict_str_str()["link"]
        scape_function = partial(_get_product_info, producer_url)
        result = driver_pool.execute(scape_function)
        return result, True


def _get_product_info(search: str, driver: WebDriver, wait: WebDriverWait[WebDriver]) -> Product:
    driver.get(search)

    # Find all img tags
    img_elements = driver.find_elements(By.TAG_NAME, "img")

    # Sort the images by size
    img_elements.sort(key=lambda x: x.size["width"] * x.size["height"], reverse=True)

    # Select the images that are at worst 1.5 times smaller than the biggest image
    max_size = img_elements[0].size["width"] * img_elements[0].size["height"]
    selected_images = [img for img in img_elements if img.size["width"] * img.size["height"] >= max_size / 1.5]

    # Get the image of these that has the top left corner closest to the top left corner of the screen
    selected_images.sort(key=lambda x: x.location["x"] + x.location["y"])
    selected_image = selected_images[0]

    # Sroll so long until the image starts to disappear from the screen
    driver.execute_script("arguments[0].scrollIntoView();", selected_image)  # type: ignore

    # Get the screen size
    screen_height = driver.execute_script("return window.innerHeight;")  # type: ignore
    screen_width = driver.execute_script("return window.innerWidth;")  # type: ignore

    # Get the size of the search field
    search_field_x, search_field_y = selected_image.location["x"], selected_image.location["y"]
    search_field_h = screen_height
    search_field_w = screen_width - search_field_x
    search_field = box(search_field_x, search_field_y, search_field_x + search_field_w, search_field_y + search_field_h)

    best_overlap = 0.0
    best = selected_image
    parent = selected_image
    while True:
        # Find the parent of the image that covers the area we are seeing best
        parent = parent.find_element(By.XPATH, "..")
        overlap = _web_element_overlap(search_field, parent)
        if overlap > best_overlap:
            best_overlap = overlap
            best = parent

        # if reached root, break
        if parent.tag_name == "html":
            break

    if best is None:
        raise ValueError("No parent found")

    # Get the inner text of the parent
    product_text = _get_visible_text(best)
    user_prompt = "Extract the information from the following blob:\n\n" + product_text
    response = ask_chat_gpt(ASSISTANT_INSTRUCTION, [USER_PROMPT, SYSTEM_ANSWER, user_prompt]).split("\n")

    product_info = {"producer_url": search}
    for line in response:
        key, value = line.split(": ", 1)
        if key in ["Price", "Original Name", "Description", "Material", "Specs"]:
            format_key = key.lower().replace(" ", "_")
            product_info[format_key] = value

    return Product(product_info, data_description="retail-price-details", data_type="dict[str,str]")  # type: ignore


def _web_element_overlap(search_field: Polygon, element: WebElement) -> float:
    elem_x, elem_y = element.location["x"], element.location["y"]
    elem_w, elem_h = element.size["width"], element.size["height"]
    element_box = box(elem_x, elem_y, elem_x + elem_w, elem_y + elem_h)
    op: float = search_field.intersection(element_box).area / search_field.union(element_box).area
    return op


def _get_visible_text(element: WebElement) -> str:
    text = element.get_attribute("innerText")
    if not text:
        return ""
    return text.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()
