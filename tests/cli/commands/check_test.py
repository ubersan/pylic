import pytest
from cleo import Application, CommandTester

from pylic.cli.commands.check import CheckCommand


@pytest.fixture
def check() -> CommandTester:
    app = Application()
    app.add(CheckCommand())

    check_command = app.find("check")
    return CommandTester(check_command)
