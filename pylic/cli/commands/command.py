class Command:
    targets: list[str]
    token: str

    def handle(self, options: list[str]) -> int:
        raise NotImplementedError()
