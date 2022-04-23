from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.cli.commands.check import CheckCommand


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch("pylic.cli.commands.check.console_writer")


@pytest.fixture
def check_command() -> CheckCommand:
    return CheckCommand()


def test_check_is_valid_if_no_packages_are_installed_and_config_is_empty(
    mocker: MockerFixture, check_command: CheckCommand, console_writer: MagicMock
) -> None:
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=[])
    return_code = check_command.handle([])
    assert return_code == 0
    console_writer.write_all_licenses_ok.assert_called()


def test_check_yields_correct_unnecessary_safe_licenses(
    mocker: MockerFixture, check_command: CheckCommand, license: str, console_writer: MagicMock
) -> None:
    safe_licenses = [f"{license}1", f"{license}2"]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=(safe_licenses, []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=[])
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unnecessary safe licenses listed which are not used by any installed package:"
    assert f"{license}1" in lines[1]
    assert f"{license}2" in lines[2]


def test_check_yields_correct_unnecessary_unsafe_packages(
    mocker: MockerFixture, check_command: CheckCommand, package: str, console_writer: MagicMock
) -> None:
    unsafe_packages = [f"{package}1", f"{package}2"]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], unsafe_packages))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=[])
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unsafe packages listed which are not installed:"
    assert f"{package}1" in lines[1]
    assert f"{package}2" in lines[2]


def test_check_yields_correct_bad_unsafe_packages(
    mocker: MockerFixture, check_command: CheckCommand, package: str, license: str, version: str, console_writer: MagicMock
) -> None:
    unsafe_packages = [f"{package}"]
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([license], unsafe_packages))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=installed_licenses)
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Found unsafe packages with a known license. Instead allow these licenses explicitly:"
    assert package in lines[1]
    assert version in lines[1]
    assert license in lines[1]


def test_check_yields_correct_missing_unsafe_packages(
    mocker: MockerFixture, check_command: CheckCommand, package: str, version: str, console_writer: MagicMock
) -> None:
    installed_licenses = [{"package": f"{package}", "license": "unknown", "version": version}]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=installed_licenses)
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Found unsafe packages:"
    assert package in lines[1]
    assert version in lines[1]


def test_check_yields_correct_unsafe_licenses(
    mocker: MockerFixture, check_command: CheckCommand, package: str, license: str, version: str, console_writer: MagicMock
) -> None:
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=installed_licenses)
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Found unsafe licenses:"
    assert package in lines[1]
    assert version in lines[1]
    assert license in lines[1]
