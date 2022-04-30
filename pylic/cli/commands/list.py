from typing import List

from pylic.cli.commands.command import Command
from pylic.cli.console_writer import BLUE, BOLD, END_STYLE, LABEL, UNDERLINE, console_writer
from pylic.licenses import read_all_installed_licenses_metadata


class ListCommand(Command):
    targets = ["list"]
    token = "list"

    def handle(self, options: List[str]) -> int:
        if "help" in options:
            self._show_help()
            return 1

        installed_licenses = read_all_installed_licenses_metadata()
        unsorted = {
            installed["package"]: {"version": installed["version"], "license": installed["license"]} for installed in installed_licenses
        }
        for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
            console_writer.line(f"{BLUE}{package}{END_STYLE} {LABEL}({rest['version']}){END_STYLE}: {rest['license']}")
        return 0

    def _show_help(self) -> None:
        console_writer.line(f"{BOLD}USAGE{END_STYLE}")
        console_writer.line(f"  {UNDERLINE}pylic{END_STYLE} {UNDERLINE}list{END_STYLE} [-h]\n")
        console_writer.line(f"{BOLD}GLOBAL OPTIONS{END_STYLE}")
        console_writer.line(f"  {LABEL}-h{END_STYLE} (--help)\tDisplay this help message\n")
        console_writer.line(f"{BOLD}DESCRIPTION{END_STYLE}")
        console_writer.line("  Lists all installed packages and their corresponding license.")
