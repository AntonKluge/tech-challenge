from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.chat_gpt import ask_chat_gpt
from lens_gpt_backend.utils.google_search import google_search
from lens_gpt_backend.utils.product import Product

ASSISTANT_INSTR = ("You are an helpful assistant which helps me to find the website of the original producer "
                   "of a specific product. I have the urls of multiple websites which showed up when I searched "
                   "for that product. They are enumerated. Please give me the number of the website which "
                   "is most likely the original producer of the product, not a reseller. I explicitly want to website"
                   "of the Producer of that specific product, none other! It is very important that you only return "
                   "the number of the website and not any other information.")

EXAMPLE_TITLES = ("Product: Patagonia Fitz Roy Trout Trucker Hat\n"
                  "1. https://eu.patagonia.com/de/de/product/fitz-roy-trout-trucker-hat/38288.html\n"
                  "2. https://zefixflyfishing.com/products/patagonia-fitz-roy-trout-trucker-hat\n"
                  "3. https://www.rudiheger.eu/fitz-roy-trout-trucker-hat-black.html\n"
                  "4. https://www.adh-fishing.de/bekleidung/kopfbedeckungen/kappen-und-huete/patagonia-fitz-roy-trout-trucker-hat-kappe-witn")

EXAMPLE_ANSWERS = "1"


class ProducerWebsite(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:

        search_dict = input_value.get_dict_str_str()
        search = search_dict["producer"] + " " + search_dict["model"]
        search_results = google_search(search)

        input_urls = [f"{i + 1}. {result['link']}" for i, result in enumerate(search_results)]
        prompt = f"Product: {search}\n{input_urls}"

        for i in range(3):
            response = ask_chat_gpt(ASSISTANT_INSTR, [EXAMPLE_TITLES, EXAMPLE_ANSWERS, prompt])
            if response.isnumeric() and 1 <= int(response) <= 7:
                return Product(search_results[int(response) - 1], data_description="producer-url", data_type="dict[str,str]"), True  # type: ignore
            print("Invalid response, please try again: " + response + "\n" + prompt)

        raise ValueError("No response from AI model!")
