from pylic.__version__ import version
from pylic.cli.commands.command import Command


class HelpCommand(Command):
    def handle(self, args: list[str]) -> int:
        return 1
