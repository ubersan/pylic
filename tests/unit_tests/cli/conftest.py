import pytest

from pylic.cli.commands.check import CheckCommand
from pylic.cli.commands.help import HelpCommand
from pylic.cli.commands.list import ListCommand
from pylic.cli.commands.version import VersionCommand
from pylic.cli.console_reader import ConsoleReader


@pytest.fixture
def console_reader(help_command: HelpCommand) -> ConsoleReader:
    return ConsoleReader(commands=[help_command])


@pytest.fixture
def check_command() -> CheckCommand:
    return CheckCommand()


@pytest.fixture
def help_command() -> HelpCommand:
    return HelpCommand()


@pytest.fixture
def list_command() -> ListCommand:
    return ListCommand()


@pytest.fixture
def version_command() -> VersionCommand:
    return VersionCommand()
