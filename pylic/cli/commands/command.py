from typing import List


class Command:
    targets: List[str]
    token: str

    def handle(self, options: List[str]) -> int:
        raise NotImplementedError()  # pragma: no cover
