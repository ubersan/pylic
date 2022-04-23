from typing import List

from pylic.__version__ import version
from pylic.cli.commands.command import Command
from pylic.cli.console_writer import END_STYLE, LABEL, console_writer


class VersionCommand(Command):
    targets = ["-V", "--version"]
    token = "version"

    def handle(self, options: List[str]) -> int:
        console_writer.line(f"Pylic version {LABEL}{version}{END_STYLE}")
        return 0
