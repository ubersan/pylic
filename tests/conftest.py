import random
import string

import pytest


def random_string() -> str:
    return "".join(random.choice(string.ascii_lowercase) for i in range(10))


@pytest.fixture
def license() -> str:
    return random_string()


@pytest.fixture
def package() -> str:
    return random_string()


@pytest.fixture
def version() -> str:
    def random_integer() -> int:
        return random.randint(0, 100)

    return f"{random_integer()}.{random_integer()}.{random_integer()}"
