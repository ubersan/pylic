from pylic.__version__ import version
from pylic.cli.commands.command import Command


class VersionCommand(Command):
    def handle(self, args: list[str]) -> int:
        print("version", version)
        return 0
