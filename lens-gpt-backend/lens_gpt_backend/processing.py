import threading
from typing import Callable

from lens_gpt_backend.producer.lens_links_producer import LensLinksProducer
from lens_gpt_backend.producer.model_information_producer import ModelInformationProducer
from lens_gpt_backend.producer.model_producer import ModelProducerProducer
from lens_gpt_backend.producer.price_producer import PriceProducer
from lens_gpt_backend.producer.producer import Producer
from lens_gpt_backend.producer.producer_website import ProducerWebsite
from lens_gpt_backend.producer.second_hand_offer_producer import SecondHandOfferProducer
from lens_gpt_backend.utils.product import Product


def process_async(file_hash: str, init: Callable[[Producer], None]) -> None:
    """
    Starts an async processing of the file.
    @param file_hash:
    @param init:
    @return:
    """
    producer = _processing_hierarchy(file_hash)
    threading.Thread(target=init, args=(producer,)).start()


def _processing_hierarchy(file_hash: str) -> Producer:

    lens_links = LensLinksProducer(file_hash, add_queue=False)
    model_producer = ModelProducerProducer(file_hash)
    model_information_producer = ModelInformationProducer(file_hash)
    price_producer = PriceProducer(file_hash)
    second_hand_offer_producer = SecondHandOfferProducer(file_hash)
    producer_website_producer = ProducerWebsite(file_hash)

    lens_links.register_producer(model_producer)
    model_producer.register_producer(producer_website_producer)
    model_producer.register_producer(second_hand_offer_producer)
    second_hand_offer_producer.register_producer(price_producer)
    producer_website_producer.register_producer(model_information_producer)

    return lens_links
