import unittest

from lens_gpt_backend.producer.second_hand_offer_producer import SecondHandOfferProducer
from lens_gpt_backend.utils.product import Product


class SecondHandOfferProducerTest(unittest.TestCase):

    def test_patagonia_tee(self) -> None:

        model_producer = {"producer": "Patagonia", "model": "Men's Long-Sleeved P-6 Logo Responsibili-Tee"}
        product = Product(model_producer, data_description="model-producer")  # type: ignore
        producer = SecondHandOfferProducer("test_hash")
        result = producer._produce(product)

        pass