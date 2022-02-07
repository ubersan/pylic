class Command:
    def handle(self, args: list[str]) -> int:
        raise NotImplementedError()
