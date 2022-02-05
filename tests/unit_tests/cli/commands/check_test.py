import pytest
from cleo import Application, CommandTester
from pytest_mock import MockerFixture

from pylic.cli.commands.check import CheckCommand


@pytest.fixture
def check() -> CommandTester:
    app = Application()
    app.add(CheckCommand())

    check_command = app.find("check")
    return CommandTester(check_command)


def test_check_is_valid_if_no_packages_are_installed_and_config_is_empty(mocker: MockerFixture, check: CommandTester) -> None:
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=[])
    return_code = check.execute()
    assert return_code == 0
    assert check.io.fetch_output() == "All licenses ok\n"
    assert check.io.fetch_error() == ""


def test_check_yields_correct_unnecessary_safe_licenses(mocker: MockerFixture, check: CommandTester, license: str) -> None:
    safe_licenses = [f"{license}1", f"{license}2"]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=(safe_licenses, []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=[])
    return_code = check.execute()
    assert return_code == 1
    assert check.io.fetch_output() == ""
    assert (
        check.io.fetch_error()
        == f"""Unnecessary safe licenses listed which are not used by any installed package:
  {license}1
  {license}2\n"""
    )


def test_check_yields_correct_unnecessary_unsafe_packages(mocker: MockerFixture, check: CommandTester, package: str) -> None:
    unsafe_packages = [f"{package}1", f"{package}2"]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], unsafe_packages))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=[])
    return_code = check.execute()
    assert return_code == 1
    assert check.io.fetch_output() == ""
    assert (
        check.io.fetch_error()
        == f"""Unsafe packages listed which are not installed:
  {package}1
  {package}2\n"""
    )


def test_check_yields_correct_bad_unsafe_packages(
    mocker: MockerFixture, check: CommandTester, package: str, license: str, version: str
) -> None:
    unsafe_packages = [f"{package}"]
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([license], unsafe_packages))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=installed_licenses)
    return_code = check.execute()
    assert return_code == 1
    assert check.io.fetch_output() == ""
    assert (
        check.io.fetch_error()
        == f"""Found unsafe packages with a known license. Instead allow these licenses explicitly:
  {package} ({version}): {license}\n"""
    )


def test_check_yields_correct_missing_unsafe_packages(mocker: MockerFixture, check: CommandTester, package: str, version: str) -> None:
    installed_licenses = [{"package": f"{package}", "license": "unknown", "version": version}]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=installed_licenses)
    return_code = check.execute()
    assert return_code == 1
    assert check.io.fetch_output() == ""
    assert (
        check.io.fetch_error()
        == f"""Found unsafe packages:
  {package} ({version})\n"""
    )


def test_check_yields_correct_unsafe_licenses(
    mocker: MockerFixture, check: CommandTester, package: str, license: str, version: str
) -> None:
    installed_licenses = [{"package": f"{package}", "license": license, "version": version}]
    mocker.patch("pylic.cli.commands.check.read_config", return_value=([], []))
    mocker.patch("pylic.cli.commands.check.read_all_installed_licenses_metadata", return_value=installed_licenses)
    return_code = check.execute()
    assert return_code == 1
    assert check.io.fetch_output() == ""
    assert (
        check.io.fetch_error()
        == f"""Found unsafe licenses:
  {package} ({version}): {license}\n"""
    )
