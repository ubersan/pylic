from typing import cast

import pytest
from cleo import Application, CommandTester
from pytest_mock import MockerFixture

from pylic.cli.commands.list import ListCommand
from tests.unit_tests.conftest import random_string


@pytest.fixture
def list_command() -> CommandTester:
    app = Application()
    app.add(ListCommand())

    list_command = app.find("list")
    return CommandTester(list_command)


def test_yields_correct_and_alphabetically_sorted_package_list(
    mocker: MockerFixture, list_command: CommandTester, license: str, version: str
) -> None:
    number_of_packages = 10
    license_metadata = [
        {"package": f"{random_string()}", "license": f"{license}{i}", "version": f"{version}{i}"}
        for i in range(0, number_of_packages)
    ]
    mocker.patch("pylic.cli.commands.list.read_all_installed_licenses_metadata", return_value=license_metadata)
    return_code = list_command.execute()
    assert return_code == 0
    assert list_command.io.fetch_error() == ""
    packages = list(map(lambda line: cast(str, line.split(" ")[0]), list_command.io.fetch_output().split("\n")))
    for i in range(0, number_of_packages - 1):  # ignore last newline
        assert packages[i] < packages[i + 1]
