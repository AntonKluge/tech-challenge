from lens_gpt_backend.generators.generators import Generators


class ProducerWebsite(Generators):

    def __init__(self, file_path: str):
        super().__init__("producer_website", file_path)

    def generate(self) -> tuple[dict[str, str], bool]:
        pass

