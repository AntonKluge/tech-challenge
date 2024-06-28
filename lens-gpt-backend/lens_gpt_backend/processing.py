import threading
from typing import Callable

from lens_gpt_backend.producer.lens_links_producer import LensLinksProducer
from lens_gpt_backend.producer.model_producer import ModelProducerProducer
from lens_gpt_backend.producer.producer import Producer
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
    lens_links = LensLinksProducer(file_hash)
    model_producer = ModelProducerProducer(file_hash)
    lens_links.register_producer(model_producer)
    return lens_links
