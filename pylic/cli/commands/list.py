from cleo import Command

from pylic.licenses import read_all_installed_licenses_metadata


class ListCommand(Command):
    name = "list"
    description = "Lists all installed packages and their corresponding license."

    def handle(self) -> None:
        installed_licenses = read_all_installed_licenses_metadata()

        unsorted = {
            installed["package"]: {"version": installed["version"], "license": installed["license"]}
            for installed in installed_licenses
        }

        for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
            self.line(f"{package} ({rest['version']}): {rest['license']}")
