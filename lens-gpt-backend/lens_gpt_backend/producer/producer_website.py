from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.utils.product import Product


class ProducerWebsite(Producer):

    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        raise NotImplementedError
