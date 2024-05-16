from typing import TypeVar, Generic

from lens_gpt_backend.consumer.consumer import Consumer

T = TypeVar('T')


class PushClientConsumer(Consumer[T], Generic[T]):

    def consume(self, t: T) -> None:
        pass
