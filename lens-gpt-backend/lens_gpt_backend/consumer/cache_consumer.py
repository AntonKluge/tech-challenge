from typing import TypeVar

from lens_gpt_backend.consumer.consumer import Consumer

T = TypeVar('T')


class CacheConsumer(Consumer[T]):

    def consume(self, t: T) -> None:
        pass
