from pylic.cli.commands.command import Command
from pylic.cli.console_writer import console_writer


class HelpCommand(Command):
    targets = ["-h", "--help"]
    token = "help"

    def handle(self, options: list[str]) -> int:
        console_writer.line("global help is HERE")
        return 1
