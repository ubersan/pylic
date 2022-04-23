from typing import List

from pylic.__version__ import version
from pylic.cli.commands.command import Command
from pylic.cli.console_writer import BOLD, END_STYLE, LABEL, UNDERLINE, console_writer


class HelpCommand(Command):
    targets = ["-h", "--help"]
    token = "help"

    def handle(self, options: List[str]) -> int:
        console_writer.line(f"Pylic version {LABEL}{version}{END_STYLE}\n")
        console_writer.line(f'{self._header("USAGE")}')
        console_writer.line(f"  {UNDERLINE}pylic{END_STYLE} [-h] [-V] <command>\n")
        console_writer.line(f'{self._header("ARGUMENTS")}')
        console_writer.line(f"  {LABEL}<command>{END_STYLE}\t\tThe command to execute\n")
        console_writer.line(f'{self._header("GLOBAL OPTIONS")}')
        console_writer.line(f"  {LABEL}-h{END_STYLE} (--help)\t\tDisplay this or a commands help message")
        console_writer.line(f"  {LABEL}-V{END_STYLE} (--version)\tDisplay this application version\n")
        console_writer.line(f'{self._header("AVAILABLE COMMANDS")}')
        console_writer.line(f"  {LABEL}check{END_STYLE}\t\t\tChecks all installed licenses")
        console_writer.line(f"  {LABEL}list{END_STYLE}\t\t\tLists all installed packages and their corresponding license\n")
        return 1

    def _header(self, text: str) -> str:
        return f"{BOLD}{text}{END_STYLE}"
