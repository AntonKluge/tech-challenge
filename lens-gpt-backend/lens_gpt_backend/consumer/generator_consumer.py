from lens_gpt_backend.consumer.consumer import Consumer


class GeneratorConsumer(Consumer[dict[str, str]]):

    def consume(self, t: dict[str, str]) -> None:
        pass
