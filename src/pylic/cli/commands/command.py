from typing import List, NamedTuple, Optional


class TargetsToToken(NamedTuple):
    targets: List[str]
    token: str


class Command:
    targets_to_token: TargetsToToken
    option_targets_to_token: Optional[List[TargetsToToken]] = None

    def handle(self, options: List[str]) -> int:
        raise NotImplementedError()  # pragma: no cover
