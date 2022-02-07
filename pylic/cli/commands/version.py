from pylic.__version__ import version
from pylic.cli.commands.command import Command
from pylic.cli.console_writer import console_writer


class VersionCommand(Command):
    targets = ["-V", "--version"]
    token = "version"

    def handle(self, options: list[str]) -> int:
        console_writer.line(f"version {version}")
        return 0
