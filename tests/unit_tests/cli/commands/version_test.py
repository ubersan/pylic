from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from pylic.__version__ import version
from pylic.cli.commands import version as version_module
from pylic.cli.commands.version import VersionCommand


@pytest.fixture
def console_writer(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(version_module, "console_writer")


def test_version(version_command: VersionCommand, console_writer: MagicMock) -> None:
    return_code = version_command.handle([])
    assert return_code == 0
    console_writer.line.assert_called_once()
    line = console_writer.line.call_args_list[0][0][0]
    assert "Pylic version" in line
    assert version in line
