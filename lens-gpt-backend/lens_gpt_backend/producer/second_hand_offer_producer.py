from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product


class SecondHandOfferProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        price1: dict[str, str] = {
            "url": "https://ebay.com/patagonia/jacket/123",
            "price": "100.0",
            "wear": "new",
        }

        price2: dict[str, str] = {
            "url": "https://ebay.com/patagonia/jacket/124",
            "price": "120.0",
            "wear": "used",
        }

        return Product([price1, price2], data_description="price"), True  # type: ignore
