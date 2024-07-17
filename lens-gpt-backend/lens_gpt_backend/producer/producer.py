from abc import abstractmethod, ABC

from lens_gpt_backend.utils.product import Product
from lens_gpt_backend.utils.result_queue import ResultQueue


class Producer(ABC):
    """
    Abstract base class for a Producer in a producer-consumer model.

    Attributes:
        _upload_hash (str): Hash representing the file associated with the producer.
        _downstream (list[Producer]): List of downstream producers to which the output will be pushed.
        _result_queue (ResultQueue | None): Queue to store the produced results.
    """

    def __init__(self, file_hash: str, add_queue: bool = True) -> None:
        """
        Initializes the Producer with a file hash and optionally adds a result queue.

        Args:
            file_hash (str): The hash representing the file associated with the producer.
            add_queue (bool): Flag indicating whether to add a result queue. Defaults to True.
        """
        self._upload_hash = file_hash
        self._downstream: list[Producer] = []
        self._result_queue: ResultQueue | None = None
        if add_queue:
            self._result_queue = ResultQueue.factory(file_hash)

        print(f"Producer[{file_hash}]: created")

    @abstractmethod
    def _produce(self, input_value: Product) -> tuple[Product, bool]:
        """
        Abstract method to be implemented by subclasses to produce an output from an input.

        Args:
            input_value (Product): The input product to be processed.

        Returns:
            tuple[Product, bool]: A tuple containing the output product and a boolean indicating success.
        """
        pass

    def produce(self, input_value: Product) -> None:
        """
        Produces an output from the given input and pushes it to the result queue and downstream producers.

        Args:
            input_value (Product): The input product to be processed.
        """
        output_value, _ = self._produce(input_value)
        if self._result_queue:
            self._result_queue.put(output_value)
        self._push_consumers(output_value)

    def register_producer(self, producer: 'Producer') -> None:
        """

        """
        self._downstream.append(producer)

    def _push_consumers(self, output_value: Product) -> None:
        for producer in self._downstream:
            producer.produce(output_value)
