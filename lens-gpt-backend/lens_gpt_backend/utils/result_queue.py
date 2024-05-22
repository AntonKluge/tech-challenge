import threading


class ResultQueue:
    """
    A class designed to manage a queue of results for multiple concurrent requests, facilitating
    efficient communication between threads. It provides capabilities to enqueue results and
    dequeue them in a thread-safe manner, allowing multiple consumers to retrieve data as it
    becomes available. The queue supports dynamic addition of results until it is explicitly
    closed, and uses a lock to ensure thread safety and a condition variable to block consumers
    when no new data is available.
    """

    def __init__(self, file_hash: str):
        self._file_hash = file_hash
        self._queue: list[dict[str, str]] = []
        self._queue_size = 0
        self._closed = False
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)
        self._request_progress: dict[str, int] = {}

    def put(self, result: dict[str, str]) -> None:
        """
        Adds a result to the queue. Threads waiting for results will be notified.

        @param result: The result to add to the queue.
        @raises ValueError: If the queue is closed.
        """
        with self._condition:
            if self._closed:
                raise ValueError("Writing to a closed queue is not allowed.")
            self._queue.append(result)
            self._queue_size += 1
            self._condition.notify_all()  # Notify all waiting threads that new data is available

    def close(self) -> None:
        """
        Closes the queue, disallowing further additions. Notifies all waiting threads to prevent
        them from waiting indefinitely.
        """
        with self._condition:
            self._closed = True
            self._condition.notify_all()  # Ensure that all waiting threads can exit

    def get_next(self, request_id: str) -> dict[str, str] | None:
        """
        Retrieves the next available result for a request. If no results are available, the
        thread will wait until new results are added or the queue is closed.
        @param request_id: The identifier of the request for which to retrieve the next result.
        @return dict[str, str] | None: The next result or None if the queue is closed and empty.
        """
        with self._condition:
            while self._request_progress.get(request_id, 0) >= self._queue_size:
                if self._closed:
                    return None  # No more items will be added, return None to indicate completion
                self._condition.wait()  # Wait for new items or closure notification

            request_progress = self._request_progress.get(request_id, 0)
            result = self._queue[request_progress]
            self._request_progress[request_id] = request_progress + 1
            return result