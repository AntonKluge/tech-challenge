from typing import TypeVar, Generic

from lens_gpt_backend.consumer.consumer import Consumer
from lens_gpt_backend.producer.producer import Producer

I = TypeVar('I')
O = TypeVar('O')


class ProducerConsumer(Consumer[I], Generic[I, O]):

    def __init__(self, producer: Producer[list[I], O], upload_hash: str):
        super().__init__(upload_hash)
        self._producer = producer

    def consume(self, input_value: I) -> None:
        self._producer.produce(input_value)
