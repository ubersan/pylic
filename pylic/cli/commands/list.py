from cleo import Command

from pylic.pylic import read_all_installed_licenses_metadata


class ListCommand(Command):  # type:ignore
    name = "list"
    description = "Lists all installed packages and their corresponding license."

    def handle(self) -> None:
        installed_licenses = read_all_installed_licenses_metadata()

        unsorted = {
            installed["package"]: {"version": installed["version"], "license": installed["license"]}
            for installed in installed_licenses
        }

        print("Installed Packages:")
        for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
            print(f"  {package}({rest['version']}): {rest['license']}")
