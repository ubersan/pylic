import sys

import pytest
from pytest_mock import MockerFixture

from pylic.cli.app import main as app

# @pytest.fixture
# def app() -> ApplicationTester:
#    return ApplicationTester(app)


def read_pyproject_file(mocker: MockerFixture, filename: str) -> None:
    with open(filename) as pyproject_test_file:
        mocker.patch("builtins.open", mocker.mock_open(read_data=pyproject_test_file.read()))


def test_check_with_a_valid_config_yields_successful_output_and_return_code(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")

    try:
        app()
    except SystemExit as system_exit:
        # return_code = app.execute("check")
        # assert app.io.fetch_error() == ""
        # assert app.io.fetch_output() == "All licenses ok\n"
        assert system_exit.code == 0


def test_check_with_a_valid_config_and_quiet_option_runs_fine(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")
    sys.argv.append("--quiet")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 0


def test_correct_error_is_returned_when_an_unnecessary_unsafe_package_is_listed(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_unsafe_package.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1
    # return_code = app.execute("check")
    # assert app.io.fetch_error() == "Unsafe packages listed which are not installed:\n  not-installed\n"
    # assert app.io.fetch_output() == ""
    # assert return_code == 1


@pytest.mark.parametrize("allow_option", ["-p", "--allow-extra-unused-packages"])
def test_correct_error_is_returned_when_an_unnecessary_unsafe_package_is_listed_but_with_allow_extra_option_set(
    mocker: MockerFixture, allow_option: str
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_unsafe_package.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")
    sys.argv.append(allow_option)

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 0


def test_correct_error_is_returned_when_an_unnecessary_safe_license_is_listed(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_safe_license.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1
    # return_code = app.execute("check")
    # assert (
    # app.io.fetch_error() == "Unnecessary safe licenses listed which are not used by any installed package:\n  Adaptive Public License\n"
    # )
    # assert app.io.fetch_output() == ""
    # assert return_code == 1


@pytest.mark.parametrize("allow_option", ["-l", "--allow-extra-safe-licenses"])
def test_correct_error_is_returned_when_an_unnecessary_safe_license_is_listed_but_with_allow_extra_option_set(
    mocker: MockerFixture, allow_option: str
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_safe_license.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")
    sys.argv.append(allow_option)

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 0


@pytest.mark.parametrize("allow_option", ["-l", "--allow-extra-safe-licenses", "-p", "--allow-extra-unused-packages"])
def test_correct_error_is_returned_when_an_unnecessary_safe_license_and_unsafe_package_is_listed_but_only_one_is_allowed(
    mocker: MockerFixture, allow_option: str
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_unsafe_package_and_safe_license.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")
    sys.argv.append(allow_option)

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1


def test_correct_error_is_returned_when_an_unnecessary_safe_license_and_unsafe_package_is_listed_and_both_are_allowed(
    mocker: MockerFixture,
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_unsafe_package_and_safe_license.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")
    sys.argv.append("-l")
    sys.argv.append("-p")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 0


def test_correct_error_is_returned_when_bad_unsafe_package(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/bad_unsafe_package.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("check")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1
    # return_code = app.execute("check")
    # assert (
    #    app.io.fetch_error()
    #    == """Found unsafe packages with a known license. Instead allow these licenses explicitly:
    # toml (0.10.2): MIT License\n"""
    # )
    # assert app.io.fetch_output() == ""
    # assert return_code == 1


def test_correct_error_is_returned_when_no_such_command(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("bogus")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1


def test_correct_error_is_returned_when_no_such_option(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("--bogus")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1


def test_correct_error_is_returned_when_help_option(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    sys.argv.clear()
    sys.argv.append("pylic")
    sys.argv.append("--help")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1


def test_correct_error_is_returned_when_no_tokens(mocker: MockerFixture) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    sys.argv.clear()
    sys.argv.append("pylic")

    try:
        app()
    except SystemExit as system_exit:
        assert system_exit.code == 1
