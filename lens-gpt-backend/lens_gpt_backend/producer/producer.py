from abc import abstractmethod, ABC
from typing import TypeVar, Generic

from lens_gpt_backend.consumer.cache_consumer import CacheConsumer
from lens_gpt_backend.consumer.consumer import Consumer
from lens_gpt_backend.consumer.producer_consumer import ProducerConsumer
from lens_gpt_backend.consumer.puhs_client_consumer import PushClientConsumer

# The type of the input that is given to work on.
I = TypeVar('I')

# The type of the output of which should be returned a list, i.e. list[O]
O = TypeVar('O')

N = TypeVar('N')


class Producer(ABC, Generic[I, O]):

    def __init__(self, upload_hash: str, pushes_client: bool = True, caches: bool = True):
        self._upload_hash = upload_hash
        self._downstream: list[Consumer[O]] = []

        if pushes_client:
            self.register_consumer(PushClientConsumer(upload_hash))

        if caches:
            self.register_consumer(CacheConsumer(upload_hash))

    @abstractmethod
    def produce(self, input_value: I) -> tuple[list[O], bool]:
        pass

    def register_consumer(self, consumer: Consumer[O]) -> None:
        self._downstream.append(consumer)

    def register_producer(self, producer: 'Producer[O, N]') -> None:
        self.register_consumer(ProducerConsumer(producer, self._upload_hash))

    def _push_consumers(self, output_value: O) -> None:
        for consumer in self._downstream:
            consumer.consume(output_value)
