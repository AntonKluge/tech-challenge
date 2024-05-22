from lens_gpt_backend.producer.producer import Producer, I, O


class ProducerWebsite(Producer[dict[str, str], dict[str, str]]):

    def produce(self, input_value: I) -> tuple[list[O], bool]:
        pass
