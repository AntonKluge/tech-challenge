from abc import ABC, abstractmethod
from queue import Queue
from typing import Generic, TypeVar

T = TypeVar('T')


class Consumer(ABC, Generic[T]):

    def __init__(self, upload_hash: str):
        self._upload_hash = upload_hash
        self._queue = Queue[T]()

    def add(self, t: T | list[T]) -> None:
        if isinstance(t, list):
            for item in t:
                self._queue.put(item)
        else:
            self._queue.put(t)
        self._notify()

    def _notify(self) -> None:
        pass  # TODO: Implement

    @abstractmethod
    def consume(self, t: T) -> None:
        pass
