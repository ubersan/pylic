from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.cli.commands.list import ListCommand
from tests.unit_tests.conftest import random_string


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("pylic.cli.commands.list.console_writer")


@pytest.fixture
def list_commandd() -> ListCommand:
    return ListCommand()


def test_yields_correct_and_alphabetically_sorted_package_list(
    mocker: MockerFixture, list_commandd: ListCommand, license: str, version: str, console_writer: MagicMock
) -> None:
    number_of_packages = 10
    license_metadata = [
        {"package": f"{random_string()}", "license": f"{license}{i}", "version": f"{version}{i}"} for i in range(0, number_of_packages)
    ]
    mocker.patch("pylic.cli.commands.list.read_all_installed_licenses_metadata", return_value=license_metadata)
    return_code = list_commandd.handle([])
    assert return_code == 0
    packages = list(map(lambda line: cast(str, line[0][0].split(" ")[0]), console_writer.line.call_args_list))
    for i in range(0, number_of_packages - 1):
        assert packages[i] < packages[i + 1]
