from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product


class ModelInformationProducer(Producer):


    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        price: dict[str, float | str] = {
            "producer_url": "www.patagonia.com/jacket",
            "retail_price": 100.0,
            "original_name": "Men's Better Sweater™ 1/4-Zip Fleece",
            "description": "A warm jacket for cold weather",
            "material": "100% polyester",
            "color": "black",
            "specs": "100% polyester fleece with a sweater-knit face and a fleece interior",
        }
        return Product(price, data_description="price", data_type="price"), True  # type: ignore
