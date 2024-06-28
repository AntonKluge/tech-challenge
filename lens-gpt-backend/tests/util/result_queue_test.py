import json
import threading
import unittest
from time import sleep
from typing import List

from lens_gpt_backend.utils.product import Product
from lens_gpt_backend.utils.result_queue import ResultQueue


class ResultQueueTests(unittest.TestCase):

    def test_put_and_get_next(self) -> None:
        queue = ResultQueue.factory("test_hash")
        results = [Product(f"{i}") for i in range(5)]
        retrieved_results: List[Product] = []
        lock = threading.Lock()

        # Function to put items into the queue
        def put_items() -> None:
            for result in results:
                queue.put(result)

        # Function to get items from the queue
        def get_items() -> None:
            nonlocal retrieved_results
            for _ in range(5):
                item = queue.get_next("request1")
                with lock:
                    if item:
                        retrieved_results.append(item)

        put_thread = threading.Thread(target=put_items)
        get_thread = threading.Thread(target=get_items)

        put_thread.start()
        get_thread.start()

        put_thread.join()
        get_thread.join()

        self.assertEqual(len(retrieved_results), 5)
        self.assertEqual(retrieved_results, results)

    def test_close_while_waiting(self) -> None:
        queue = ResultQueue.factory("test_hash_close")
        results = [Product(f"{i}") for i in range(5)]
        retrieved_results: List[Product] = []
        lock = threading.Lock()

        # Function to put items into the queue
        def put_items() -> None:
            for result in results:
                queue.put(result)

        # Function to get items from the queue
        def get_items() -> None:
            nonlocal retrieved_results
            for _ in range(5):
                item = queue.get_next("request1")
                if item:
                    with lock:
                        retrieved_results.append(item)

        put_thread = threading.Thread(target=put_items)
        get_thread = threading.Thread(target=get_items)

        put_thread.start()
        get_thread.start()

        put_thread.join()
        queue.close()  # Close the queue while the get thread is waiting
        get_thread.join()

        self.assertEqual(len(retrieved_results), 5)
        self.assertEqual(retrieved_results, results)

    def test_str_generator(self) -> None:
        queue = ResultQueue.factory("test_hash_gen")
        results = [Product(f"{i}") for i in range(5)]
        retrieved_results: List[str] = []
        lock = threading.Lock()

        # Function to put items into the queue
        def put_items() -> None:
            for result in results:
                sleep(0.1)
                queue.put(result)
            queue.close()  # Add a None item to indicate the end of the queue

        # Function to generate items from the queue
        def generate_items() -> None:
            nonlocal retrieved_results
            generator = queue.str_generator("request1")
            for item in generator:
                with lock:
                    retrieved_results.append(item)

        put_thread = threading.Thread(target=put_items)
        gen_thread = threading.Thread(target=generate_items)

        put_thread.start()
        gen_thread.start()

        put_thread.join()
        gen_thread.join()

        self.assertEqual(len(retrieved_results), 5)
        for i in range(5):
            self.assertEqual(json.loads(retrieved_results[i]), json.loads(results[i].json()))

    def test_is_fresh(self) -> None:
        queue = ResultQueue.factory("test_hash_fresh")

        self.assertTrue(queue.is_fresh())

        result = Product("test")
        queue.put(result)

        self.assertFalse(queue.is_fresh())

        queue.close()
        self.assertFalse(queue.is_fresh())


if __name__ == '__main__':
    unittest.main()
