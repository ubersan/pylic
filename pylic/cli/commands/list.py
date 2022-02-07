from pylic.cli.commands.command import Command
from pylic.licenses import read_all_installed_licenses_metadata


class ListCommand(Command):
    def handle(self, args: list[str]) -> int:
        installed_licenses = read_all_installed_licenses_metadata()

        unsorted = {
            installed["package"]: {"version": installed["version"], "license": installed["license"]} for installed in installed_licenses
        }

        for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
            print(f"{package} ({rest['version']}): {rest['license']}")

        return 0
