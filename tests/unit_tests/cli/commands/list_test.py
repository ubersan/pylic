from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.cli.commands import list as list_module
from pylic.cli.commands.list import ListCommand
from tests.unit_tests.conftest import random_string


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(list_module, "console_writer")


def test_help(list_command: ListCommand, console_writer: MagicMock) -> None:
    return_code = list_command.handle(["help"])
    assert return_code == 1
    console_writer.line.assert_called()
    assert "USAGE" in console_writer.line.call_args_list[0][0][0]


def test_yields_correct_and_alphabetically_sorted_package_list(
    mocker: MockerFixture, list_command: ListCommand, license: str, version: str, console_writer: MagicMock
) -> None:
    number_of_packages = 10
    license_metadata = [
        {"package": f"{random_string()}", "license": f"{license}{i}", "version": f"{version}{i}"} for i in range(0, number_of_packages)
    ]
    mocker.patch("pylic.cli.commands.list.read_all_installed_licenses_metadata", return_value=license_metadata)
    return_code = list_command.handle([])
    assert return_code == 0
    packages = list(map(lambda line: cast(str, line[0][0].split(" ")[0]), console_writer.line.call_args_list))
    for i in range(0, number_of_packages - 1):
        assert packages[i] < packages[i + 1]
