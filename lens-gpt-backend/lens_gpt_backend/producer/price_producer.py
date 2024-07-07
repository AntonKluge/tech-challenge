from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product


class PriceProducer(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        price: dict[str, float | str] = {
            "price": 100.0,
            "certainty": "high",
            "min_range": 90.0,
            "max_range": 110.0,
        }
        return Product(price, data_description="estimated-price", data_type="price"), True  # type: ignore
