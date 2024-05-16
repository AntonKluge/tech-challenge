from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from lens_gpt_backend.producer.producer import Producer

T = TypeVar('T')


class Consumer(ABC, Generic[T]):

    def __init__(self, upload_hash: str):
        self._upload_hash = upload_hash
        self._upstreams: list[Producer[T]] = []

    @abstractmethod
    def consume(self, t: T) -> None:
        pass

    def register_producer(self, upstream: Producer[T]) -> None:
        self._upstreams.append(upstream)
