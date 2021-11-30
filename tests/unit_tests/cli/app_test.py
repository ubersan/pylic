from unittest.mock import MagicMock

import pytest
from cleo import ApplicationTester
from pytest_mock import MockerFixture

from pylic.cli.app import app


@pytest.fixture
def test_app() -> ApplicationTester:
    return ApplicationTester(app)


def test_app_shows_help_message_by_default(test_app: ApplicationTester) -> None:
    return_code = test_app.execute("")
    assert return_code == 1
    default_output = test_app.io.fetch_output()
    test_app.io.clear_output()
    test_app.execute("help")
    help_output = test_app.io.fetch_output()
    assert default_output == help_output


def test_app_shows_correct_help_message(test_app: ApplicationTester) -> None:
    test_app = ApplicationTester(app)
    return_code = test_app.execute("help")
    assert return_code == 1
    help_output = test_app.io.fetch_output()
    assert help_output == (
        """Pylic version 2.2.0

USAGE
  pylic <command>

ARGUMENTS
  <command>\tThe command to execute

AVAILABLE COMMANDS
  check\t\tChecks all installed licenses
  help\t\tDisplays this help message
  list\t\tLists all installed packages and their corresponding license
"""
    )


def test_app_accepts_the_check_command(mocker: MockerFixture, test_app: ApplicationTester) -> None:
    mocker.patch("pylic.cli.app.CheckCommand", return_value=MagicMock)
    return_code = test_app.execute("check")
    assert return_code == 0


def test_app_accepts_the_list_command(mocker: MockerFixture, test_app: ApplicationTester) -> None:
    mocker.patch("pylic.cli.app.CheckCommand", return_value=MagicMock)
    return_code = test_app.execute("check")
    assert return_code == 0
