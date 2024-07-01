from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product


class ProducerWebsite(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        return Product("www.patagonia.com/jacket", data_description="producer-url", data_type="url"), True
