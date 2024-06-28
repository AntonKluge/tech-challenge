from abc import abstractmethod, ABC

from lens_gpt_backend.utils.product import Product
from lens_gpt_backend.utils.result_queue import ResultQueue


class Producer(ABC):

    def __init__(self, upload_hash: str, add_queue: bool = True) -> None:
        self._upload_hash = upload_hash
        self._downstream: list[Producer] = []

        if add_queue:
            self._result_queue = ResultQueue.factory(upload_hash)

    @abstractmethod
    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        pass

    def produce(self, input_value: Product) -> None:
        output_value, more = self._produce(input_value)
        self._push_consumers(output_value)
        if self._result_queue:
            self._result_queue.put(output_value)

    def register_producer(self, producer: 'Producer') -> None:
        self._downstream.append(producer)

    def _push_consumers(self, output_value: Product) -> None:
        for producer in self._downstream:
            producer.produce(output_value)
