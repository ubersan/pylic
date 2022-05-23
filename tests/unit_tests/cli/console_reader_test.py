from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.cli import console_reader as console_reader_module
from pylic.cli.console_reader import ConsoleReader


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(console_reader_module, "console_writer")


def test_no_such_command(console_writer: MagicMock, console_reader: ConsoleReader) -> None:
    with pytest.raises(SystemExit):
        console_reader.get_program(["bogus"])
    console_writer.write_no_such_command.assert_called_with("bogus")


def test_no_such_option(console_writer: MagicMock, console_reader: ConsoleReader) -> None:
    with pytest.raises(SystemExit):
        console_reader.get_program(["--bogus"])
    console_writer.write_no_such_option.assert_called_with("--bogus")
