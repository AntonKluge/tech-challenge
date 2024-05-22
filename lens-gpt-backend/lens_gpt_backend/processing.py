from typing import Callable

from lens_gpt_backend.producer.lens_links_producer import LensLinksProducer
from lens_gpt_backend.producer.model_producer import ModelProducerProducer


def process_request(file_path: str, client_push: Callable[[str], None]) -> None:
    pass


def _processing_hierarch(file_path: str) -> None:
    lens_links = LensLinksProducer(file_path)
    model_producer = ModelProducerProducer(file_path)
    lens_links.register_producer(model_producer)
