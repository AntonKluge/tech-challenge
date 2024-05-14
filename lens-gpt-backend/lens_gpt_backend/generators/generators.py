from abc import abstractmethod, ABC
from typing import Generator


class Generators(ABC):

    def __init__(self, name: str, file_path: str):
        self._name = name
        self._file_path = file_path
        self._generator = None

    @abstractmethod
    def generate(self) -> tuple[dict[str, str], bool]:
        pass

    def get_generator(self) -> Generator[dict[str, str], None, None]:
        if self._generator is None:
            self._generator = self._init_generator()
        return self._generator

    def _init_generator(self) -> Generator[dict[str, str], None, None]:
        while True:
            result, done = self.generate()
            yield result
            if done:
                break


class DownStreamGenerators(Generators):

    def __init__(self, name: str, file_path: str, upstream_generator: Generator[dict[str, str], None, None]):
        super().__init__(name, file_path)
        self._upstream_generator = upstream_generator

    def generate(self) -> tuple[dict[str, str], bool]:
        upstream_result = next(self._upstream_generator)
        return self._process(upstream_result), True if upstream_result is None else False

    @abstractmethod
    def _process(self, upstream_result: dict[str, str]) -> dict[str, str]:
        pass