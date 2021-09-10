import sys

from cleo import Command

from pylic.pylic import (
    check_for_unnecessary_safe_licenses,
    check_for_unnecessary_unsafe_packages,
    check_licenses,
    check_unsafe_packages,
    read_all_installed_licenses_metadata,
)
from pylic.toml import read_config


class CheckCommand(Command):  # type:ignore
    name = "check"
    description = "Checks all installed licenses."

    def handle(self) -> None:
        safe_licenses, unsafe_packages = read_config()
        installed_licenses = read_all_installed_licenses_metadata()
        no_unnecessary_safe_licenses = check_for_unnecessary_safe_licenses(safe_licenses, installed_licenses)
        no_unncessary_unsafe_packages = check_for_unnecessary_unsafe_packages(unsafe_packages, installed_licenses)
        packages_ok = check_unsafe_packages(unsafe_packages, installed_licenses)
        licenses_ok = check_licenses(safe_licenses, installed_licenses)

        if all([no_unnecessary_safe_licenses, no_unncessary_unsafe_packages, packages_ok, licenses_ok]):
            print("All licenses ok")
        else:
            sys.exit(1)
