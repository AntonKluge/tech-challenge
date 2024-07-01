import threading
from typing import Generator, Optional

from lens_gpt_backend.utils.product import Product


class ResultQueue:
    """
    A class designed to manage a queue of results for multiple concurrent requests, facilitating
    efficient communication between threads. It provides capabilities to enqueue results and
    dequeue them in a thread-safe manner, allowing multiple consumers to retrieve data as it
    becomes available. The queue supports dynamic addition of results until it is explicitly
    closed, and uses a lock to ensure thread safety and a condition variable to block consumers
    when no new data is available.
    """

    _result_queues: dict[str, 'ResultQueue'] = {}

    @staticmethod
    def _get_result_queue(file_hash: str) -> Optional['ResultQueue']:
        """
        Retrieves the result queue for a given file hash. If the queue does not exist, it will be
        created and stored for future access.

        @param file_hash: The hash of the file for which to retrieve the result queue.
        @return ResultQueue: The result queue for the given file hash.
        """
        if file_hash not in ResultQueue._result_queues:
            return None
        return ResultQueue._result_queues[file_hash]

    @staticmethod
    def factory(file_hash: str) -> 'ResultQueue':
        """
        Factory method to create a new ResultQueue instance or retrieve an existing one.

        @param file_hash: The hash of the file for which to create or retrieve the result queue.
        @return ResultQueue: The result queue for the given file hash.
        """
        result_queue = ResultQueue._get_result_queue(file_hash)
        if result_queue is None:
            result_queue = ResultQueue(file_hash)
            ResultQueue._result_queues[file_hash] = result_queue
        else:
            result_queue._fresh = False
        return result_queue

    def __init__(self, file_hash: str) -> None:
        self._file_hash = file_hash
        self._queue: list[Product] = []
        self._queue_size = 0
        self._closed = False
        self._fresh = True
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._request_progress: dict[str, int] = {}

    def put(self, result: Product) -> None:
        """
        Adds a result to the queue. Threads waiting for results will be notified.

        @param result: The result to add to the queue.
        @raises ValueError: If the queue is closed.
        """
        print(
            f"ResultQueue[{self._file_hash}]: trying to put {result} by {threading.current_thread().name} into {hex(id(self))}")
        with self._condition:
            if self._closed:
                raise ValueError("Writing to a closed queue is not allowed.")
            self._queue.append(result)
            self._queue_size += 1
            self._condition.notify_all()  # Notify all waiting threads that new data is available

        print(f"ResultQueue[{self._file_hash}]: put {result} by {threading.current_thread().name} into {hex(id(self))}")

    def close(self) -> None:
        """
        Closes the queue, disallowing further additions. Notifies all waiting threads to prevent
        them from waiting indefinitely.
        """
        with self._condition:
            self._closed = True
            self._condition.notify_all()  # Ensure that all waiting threads can exit

    def get_next(self, request_id: str) -> Product | None:
        """
        Retrieves the next available result for a request. If no results are available, the
        thread will wait until new results are added or the queue is closed.
        @param request_id: The identifier of the request for which to retrieve the next result.
        @return dict[str, str] | None: The next result or None if the queue is closed and empty.
        """
        print(
            f"ResultQueue[{self._file_hash}]: trying to get {request_id} by {threading.current_thread().name} from {hex(id(self))}")
        with self._condition:
            while self._request_progress.get(request_id, 0) >= self._queue_size:
                if self._closed:
                    return None  # No more items will be added, return None to indicate completion
                print(f"ResultQueue[{self._file_hash}]: wait {request_id} by {threading.current_thread().name}")
                self._condition.wait()  # Wait for new items or closure notification

            request_progress = self._request_progress.get(request_id, 0)
            result = self._queue[request_progress]
            self._request_progress[request_id] = request_progress + 1
            return result

    def is_fresh(self) -> bool:
        """
        Returns whether the queue is fresh, i.e., it has not been closed and has no results.
        @return bool: True if the queue is fresh, False otherwise.
        """
        return self._fresh

    def set_fresh(self, fresh: bool) -> None:
        self._fresh = fresh

    def str_generator(self, request_id: str) -> Generator[str, None, None]:
        """
        A generator that yields results from the queue as they become available. The generator will
        continue to yield results until the queue is closed and empty.
        @yield dict[str, str]: The next available result in the queue.
        """
        while True:
            result = self.get_next(request_id)
            if result is None:
                break
            print(f"ResultQueue[{self._file_hash}]: yield {result}")
            yield result.json()
