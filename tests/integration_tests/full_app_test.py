import pytest
from cleo import ApplicationTester
from pytest_mock import MockerFixture

from pylic.cli.app import app


@pytest.fixture
def test_app() -> ApplicationTester:
    return ApplicationTester(app)


def read_pyproject_file(mocker: MockerFixture, filename: str) -> None:
    with open(filename, "r") as pyproject_test_file:
        mocker.patch("builtins.open", mocker.mock_open(read_data=pyproject_test_file.read()))


def test_check_with_a_valid_config_yields_successful_output_and_return_code(
    mocker: MockerFixture, test_app: ApplicationTester
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/valid.toml")
    return_code = test_app.execute("check")
    assert test_app.io.fetch_error() == ""
    assert test_app.io.fetch_output() == "All licenses ok\n"
    assert return_code == 0


def test_correct_error_is_returned_when_an_unnecessary_unsafe_package_is_listed(
    mocker: MockerFixture, test_app: ApplicationTester
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_unsafe_package.toml")
    return_code = test_app.execute("check")
    assert test_app.io.fetch_error() == "Unsafe packages listed which are not installed:\n  not-installed\n"
    assert test_app.io.fetch_output() == ""
    assert return_code == 1


def test_correct_error_is_returned_when_an_unnecessary_safe_license_is_listed(
    mocker: MockerFixture, test_app: ApplicationTester
) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/unnecessary_safe_license.toml")
    return_code = test_app.execute("check")
    assert (
        test_app.io.fetch_error()
        == "Unnecessary safe licenses listed which are not used by any installed package:\n  Adaptive Public License\n"
    )
    assert test_app.io.fetch_output() == ""
    assert return_code == 1


def test_correct_error_is_returned_when_bad_unsafe_package(mocker: MockerFixture, test_app: ApplicationTester) -> None:
    read_pyproject_file(mocker, "tests/integration_tests/test_tomls/bad_unsafe_package.toml")
    return_code = test_app.execute("check")
    assert (
        test_app.io.fetch_error()
        == """Found unsafe packages with a known license. Instead allow these licenses explicitly:
  toml (0.10.2): MIT License\n"""
    )
    assert test_app.io.fetch_output() == ""
    assert return_code == 1
