from lens_gpt_backend.producer.lens_links_producer import LensLinksProducer
from lens_gpt_backend.producer.model_producer import ModelProducerProducer
from lens_gpt_backend.producer.producer import Producer


def process_request(file_path: str, ) -> None:
    pass


def _processing_hierarchy(file_path: str) -> Producer:
    lens_links = LensLinksProducer(file_path)
    model_producer = ModelProducerProducer(file_path)
    lens_links.register_producer(model_producer)

    return lens_links
