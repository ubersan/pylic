from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.cli.commands import check as check_module
from pylic.cli.commands.check import CheckCommand
from pylic.toml import AppConfig


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(check_module, "console_writer")


@pytest.fixture(autouse=True)
def read_config(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(check_module, "read_config", MagicMock(return_value=AppConfig([], [], [])))


@pytest.fixture(autouse=True)
def read_all_installed_licenses_metadata(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(check_module, "read_all_installed_licenses_metadata", MagicMock(return_value=[]))


def test_help(check_command: CheckCommand, console_writer: MagicMock) -> None:
    return_code = check_command.handle(["help"])
    assert return_code == 1
    console_writer.line.assert_called()
    assert "USAGE" in console_writer.line.call_args_list[0][0][0]


def test_check_is_valid_if_no_packages_are_installed_and_config_is_empty(check_command: CheckCommand, console_writer: MagicMock) -> None:
    return_code = check_command.handle([])
    assert return_code == 0
    console_writer.write_all_licenses_ok.assert_called()


def test_check_yields_correct_unnecessary_safe_licenses_and_status_code_is_1(
    check_command: CheckCommand,
    license: str,
    console_writer: MagicMock,
    read_config: MagicMock,
) -> None:
    safe_licenses = [f"{license}1", f"{license}2"]
    read_config.return_value = AppConfig(safe_licenses, [], [])
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unnecessary safe licenses listed which are not used by any installed package:"
    assert f"{license}1" in lines[1]
    assert f"{license}2" in lines[2]


def test_check_yields_correct_unnecessary_safe_licenses_warnings_but_status_code_is_0_if_correct_option_is_set(
    check_command: CheckCommand,
    license: str,
    console_writer: MagicMock,
    read_config: MagicMock,
) -> None:
    safe_licenses = [f"{license}1", f"{license}2"]
    read_config.return_value = AppConfig(safe_licenses, [], [])
    return_code = check_command.handle(["allow_extra_licenses"])
    assert return_code == 0
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unnecessary safe licenses listed which are not used by any installed package:"
    assert f"{license}1" in lines[1]
    assert f"{license}2" in lines[2]


def test_check_yields_correct_unnecessary_safe_licenses_warnings_but_status_code_is_1_if_wrong_option_is_set(
    check_command: CheckCommand,
    license: str,
    console_writer: MagicMock,
    read_config: MagicMock,
) -> None:
    safe_licenses = [f"{license}1", f"{license}2"]
    read_config.return_value = AppConfig(safe_licenses, [], [])
    return_code = check_command.handle(["allow_extra_packages"])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unnecessary safe licenses listed which are not used by any installed package:"
    assert f"{license}1" in lines[1]
    assert f"{license}2" in lines[2]


@pytest.mark.parametrize("package_ignored", [True, False])
def test_check_yields_correct_unnecessary_unsafe_packages_and_status_code_is_1(
    check_command: CheckCommand,
    package: str,
    console_writer: MagicMock,
    package_ignored: bool,
    read_config: MagicMock,
) -> None:
    unsafe_packages = [f"{package}1", f"{package}2"]
    ignore_packages = [unsafe_packages[0]] if package_ignored else []
    read_config.return_value = AppConfig([], unsafe_packages, ignore_packages)
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unsafe packages listed which are not installed:"
    assert f"{package}1" in lines[1]
    assert f"{package}2" in lines[2]


@pytest.mark.parametrize("package_ignored", [True, False])
def test_check_yields_correct_unnecessary_unsafe_packages_but_status_code_is_0_if_correct_option_is_set(
    check_command: CheckCommand,
    package: str,
    console_writer: MagicMock,
    package_ignored: bool,
    read_config: MagicMock,
) -> None:
    unsafe_packages = [f"{package}1", f"{package}2"]
    ignore_packages = [unsafe_packages[0]] if package_ignored else []
    read_config.return_value = AppConfig([], unsafe_packages, ignore_packages)
    return_code = check_command.handle(["allow_extra_packages"])
    assert return_code == 0
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unsafe packages listed which are not installed:"
    assert f"{package}1" in lines[1]
    assert f"{package}2" in lines[2]


@pytest.mark.parametrize("package_ignored", [True, False])
def test_check_yields_correct_unnecessary_unsafe_packages_but_status_code_is_1_if_wrong_option_is_set(
    check_command: CheckCommand,
    package: str,
    console_writer: MagicMock,
    package_ignored: bool,
    read_config: MagicMock,
) -> None:
    unsafe_packages = [f"{package}1", f"{package}2"]
    ignore_packages = [unsafe_packages[0]] if package_ignored else []
    read_config.return_value = AppConfig([], unsafe_packages, ignore_packages)
    return_code = check_command.handle(["allow_extra_licenses"])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unsafe packages listed which are not installed:"
    assert f"{package}1" in lines[1]
    assert f"{package}2" in lines[2]


@pytest.mark.parametrize("package_ignored", [True, False])
def test_check_yields_correct_unnecessary_unsafe_packages_and_safe_licenses_but_status_code_is_0_if_correct_options_are_set(
    check_command: CheckCommand,
    package: str,
    console_writer: MagicMock,
    package_ignored: bool,
    read_config: MagicMock,
) -> None:
    safe_licenses = [f"{license}1", f"{license}2"]
    unsafe_packages = [f"{package}1", f"{package}2"]
    ignore_packages = [unsafe_packages[0]] if package_ignored else []
    read_config.return_value = AppConfig(safe_licenses, unsafe_packages, ignore_packages)
    return_code = check_command.handle(["allow_extra_packages", "allow_extra_licenses"])
    assert return_code == 0
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Unnecessary safe licenses listed which are not used by any installed package:"
    assert f"{license}1" in lines[1]
    assert f"{license}2" in lines[2]
    assert lines[3] == "Unsafe packages listed which are not installed:"
    assert f"{package}1" in lines[4]
    assert f"{package}2" in lines[5]


def test_check_yields_correct_unnecessary_ignore_packages(
    check_command: CheckCommand,
    package: str,
    console_writer: MagicMock,
    read_config: MagicMock,
) -> None:
    ignore_packages = [f"{package}1", f"{package}2"]
    read_config.return_value = AppConfig([], [], ignore_packages)
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Ignore packages listed which are not installed:"
    assert f"{package}1" in lines[1]
    assert f"{package}2" in lines[2]


@pytest.mark.parametrize("package_ignored", [True, False])
def test_check_yields_correct_bad_unsafe_packages(
    check_command: CheckCommand,
    package: str,
    license: str,
    version: str,
    console_writer: MagicMock,
    package_ignored: bool,
    read_config: MagicMock,
    read_all_installed_licenses_metadata: MagicMock,
) -> None:
    unsafe_packages = [f"{package}"]
    ignore_packages = unsafe_packages if package_ignored else []
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    read_config.return_value = AppConfig([license], unsafe_packages, ignore_packages)
    read_all_installed_licenses_metadata.return_value = installed_licenses
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Found unsafe packages with a known license. Instead allow these licenses explicitly:"
    assert package in lines[1]
    assert version in lines[1]
    assert license in lines[1]


@pytest.mark.parametrize("package_ignored", [True, False])
def test_check_yields_correct_missing_unsafe_packages(
    check_command: CheckCommand,
    package: str,
    version: str,
    console_writer: MagicMock,
    package_ignored: bool,
    read_config: MagicMock,
    read_all_installed_licenses_metadata: MagicMock,
) -> None:
    ignore_packages = [f"{package}"] if package_ignored else []
    installed_licenses = [{"package": f"{package}", "license": "unknown", "version": version}]
    read_config.return_value = AppConfig([], [], ignore_packages)
    read_all_installed_licenses_metadata.return_value = installed_licenses
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Found unsafe packages:"
    assert package in lines[1]
    assert version in lines[1]


def test_check_yields_correct_unsafe_licenses(
    check_command: CheckCommand,
    package: str,
    license: str,
    version: str,
    console_writer: MagicMock,
    read_config: MagicMock,
    read_all_installed_licenses_metadata: MagicMock,
) -> None:
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    read_config.return_value = AppConfig([], [], [])
    read_all_installed_licenses_metadata.return_value = installed_licenses
    return_code = check_command.handle([])
    assert return_code == 1
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Found unsafe licenses:"
    assert package in lines[1]
    assert version in lines[1]
    assert license in lines[1]


def test_check_yields_correct_unsafe_licenses_when_packages_ignored(
    check_command: CheckCommand,
    package: str,
    license: str,
    version: str,
    console_writer: MagicMock,
    read_config: MagicMock,
    read_all_installed_licenses_metadata: MagicMock,
) -> None:
    ignore_packages = [f"{package}"]
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    read_config.return_value = AppConfig([], [], ignore_packages)
    read_all_installed_licenses_metadata.return_value = installed_licenses
    return_code = check_command.handle([])
    assert return_code == 0
    console_writer.write_all_licenses_ok.assert_called()
    lines = list(map(lambda line: cast(str, line[0][0]), console_writer.line.call_args_list))
    assert lines[0] == "Ignored packages with unsafe licenses:"
    assert package in lines[1]
    assert version in lines[1]
    assert license in lines[1]
