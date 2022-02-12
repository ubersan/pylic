import sys
from typing import Optional, TextIO

LABEL = "\033[96m"
SUCCESS = "\033[92m"
BLUE = "\033[94m"
WARNING = "\033[93m"
ERROR = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_STYLE = "\033[0m"


class ConsoleWriter:
    def __init__(self, stream: Optional[TextIO] = None) -> None:
        self.stream = stream or sys.stdout

    def write_no_such_command(self, command: str) -> None:
        self.line(f'{ERROR}{BOLD}The command "{command}" is not available.{END_STYLE}')

    def write_no_such_option(self, option: str) -> None:
        self.line(f'{ERROR}{BOLD}The option "{option}" is not available.{END_STYLE}')

    def write_all_licenses_ok(self) -> None:
        self.line(f"{WARNING}{BOLD}✨{END_STYLE} {SUCCESS}All licenses ok{END_STYLE} {WARNING}{BOLD}✨{END_STYLE}")

    def line(self, line: str) -> None:
        self.stream.write(f"{line}\n")
        self.stream.flush()


console_writer = ConsoleWriter()
