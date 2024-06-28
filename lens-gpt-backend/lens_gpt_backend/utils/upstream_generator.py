import json
from queue import Queue
from typing import Generator, Tuple


class UpstreamGenerator:

    def __init__(self) -> None:
        self.queue: Queue[Tuple[str, str]] = Queue()

    def push(self, item: str, item_type: str) -> None:
        self.queue.put((item, item_type))

    def generator(self) -> Generator[str, None, None]:
        while True:
            item, item_type = self.queue.get()
            if item is None:
                break

            dict_data = {"data": item, "type": item_type}
            json_str = json.dumps(dict_data)
            yield json_str
