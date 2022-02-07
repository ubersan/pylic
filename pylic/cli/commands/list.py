from pylic.cli.commands.command import Command
from pylic.cli.console_writer import console_writer
from pylic.licenses import read_all_installed_licenses_metadata


class ListCommand(Command):
    targets = ["list"]
    token = "list"

    def handle(self, options: list[str]) -> int:
        installed_licenses = read_all_installed_licenses_metadata()

        unsorted = {
            installed["package"]: {"version": installed["version"], "license": installed["license"]} for installed in installed_licenses
        }

        for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
            console_writer.line(f"{package} ({rest['version']}): {rest['license']}")

        return 0
