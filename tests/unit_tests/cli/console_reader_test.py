from typing import cast
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.cli import console_reader as console_reader_module
from pylic.cli.commands.help import HelpCommand
from pylic.cli.commands.list import ListCommand
from pylic.cli.console_reader import ConsoleReader
from pylic.cli.console_writer import ConsoleWriter


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(console_reader_module, "console_writer")


@pytest.fixture
def stream(mocker: MockerFixture) -> MagicMock:
    stream = MagicMock()
    mocker.patch.object(console_reader_module, "console_writer", new=ConsoleWriter(stream))
    return stream


@pytest.fixture
def console_reader_with_list_command(help_command: HelpCommand, list_command: ListCommand) -> ConsoleReader:
    return ConsoleReader(commands=[help_command, list_command])


def test_no_such_command(console_writer: MagicMock, console_reader: ConsoleReader) -> None:
    with pytest.raises(SystemExit):
        console_reader.get_program(["bogus"])
    console_writer.write_no_such_command.assert_called_with("bogus")


def test_no_such_option(console_writer: MagicMock, console_reader: ConsoleReader) -> None:
    with pytest.raises(SystemExit):
        console_reader.get_program(["--bogus"])
    console_writer.write_no_such_option.assert_called_with("--bogus")


def test_write_no_such_option_for_command(stream: MagicMock, console_reader_with_list_command: ConsoleReader) -> None:
    with pytest.raises(SystemExit):
        console_reader_with_list_command.get_program(["list", "--not-an-option"])
    lines = list(map(lambda line: cast(str, line[0][0]), stream.write.call_args_list))
    assert len(lines) == 1
    assert 'The option "--not-an-option" is not available for command "list".' in lines[0]


def test_write_invalid_input(stream: MagicMock, console_reader: ConsoleReader) -> None:
    with pytest.raises(SystemExit):
        console_reader.get_program(["check", "-lp", "2"])
    lines = list(map(lambda line: cast(str, line[0][0]), stream.write.call_args_list))
    assert len(lines) == 1
    assert 'Could not make sense of invalid input "2".' in lines[0]


def test_command_options_are_correctly_parsed_into_the_program(console_reader_with_list_command: ConsoleReader) -> None:
    program = console_reader_with_list_command.get_program(["list", "-h"])
    assert program.options == ["help"]
