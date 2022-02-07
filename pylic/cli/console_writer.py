import sys
from typing import Optional, TextIO

from pylic.__version__ import version

LABEL = "\033[96m"
SUCCESS = "\033[92m"
WARNING = "\033[93m"
ERROR = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_STYLE = "\033[0m"


class ConsoleWriter:
    def __init__(self, stream: Optional[TextIO] = None) -> None:
        self.stream = stream or sys.stdout

    def write_global_help(
        self,
    ) -> None:
        self.line(f"Pylic version {self._label(version)}\n")
        self.line(f'{self._header("USAGE")}')
        self.line(f"  {UNDERLINE}pylic{END_STYLE} [-h] [-V] <command>\n")
        self.line(f'{self._header("ARGUMENTS")}')
        self.line(f"  {LABEL}<command>{END_STYLE}\t\tThe command to execute\n")
        self.line(f'{self._header("GLOBAL OPTIONS")}')
        self.line(f"  {LABEL}-h{END_STYLE} (--help)\t\tDisplay this or a commands help message")
        self.line(f"  {LABEL}-V{END_STYLE} (--version)\tDisplay this application version\n")
        self.line(f'{self._header("AVAILABLE COMMANDS")}')
        self.line(f"  {LABEL}check{END_STYLE}\t\t\tChecks all installed licenses")
        self.line(f"  {LABEL}list{END_STYLE}\t\t\tLists all installed packages and their corresponding license\n")

    def write_no_such_command(self, command: str) -> None:
        self.line(f'{ERROR}{BOLD}The command "{command}" is not available.{END_STYLE}')

    def write_no_such_option(self, option: str) -> None:
        self.line(f'{ERROR}{BOLD}The option "{option}" is not available.{END_STYLE}')

    def write_all_licenses_ok(self) -> None:
        self.line(f"{WARNING}{BOLD}✨{END_STYLE} {SUCCESS}All licenses ok{END_STYLE} {WARNING}{BOLD}✨{END_STYLE}")

    def line(self, line: str) -> None:
        self.stream.write(f"{line}\n")
        self.stream.flush()

    def _label(self, text: str) -> str:
        return f"{LABEL}{text}{END_STYLE}"

    def _header(self, text: str) -> str:
        return f"{BOLD}{text}{END_STYLE}"


console_writer = ConsoleWriter()
