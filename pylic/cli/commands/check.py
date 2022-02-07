from pylic.cli.commands.command import Command
from pylic.license_checker import LicenseChecker
from pylic.licenses import read_all_installed_licenses_metadata
from pylic.toml import read_config


class CheckCommand(Command):
    def handle(self, *args) -> int:
        safe_licenses, unsafe_packages = read_config()
        installed_licenses = read_all_installed_licenses_metadata()
        checker = LicenseChecker(safe_licenses, unsafe_packages, installed_licenses)

        unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
        unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
        bad_unsafe_packages = checker.get_bad_unsafe_packages()
        missing_unsafe_packages = checker.get_missing_unsafe_packages()
        unsafe_licenses = checker.get_unsafe_licenses()

        if any(
            [
                unnecessary_safe_licenses,
                unnecessary_unsafe_packages,
                bad_unsafe_packages,
                missing_unsafe_packages,
                unsafe_licenses,
            ]
        ):
            if len(unnecessary_safe_licenses) > 0:
                print("Unnecessary safe licenses listed which are not used by any installed package:")
                for unnecessary_safe_license in unnecessary_safe_licenses:
                    print(f"  {unnecessary_safe_license}")

            if len(unnecessary_unsafe_packages) > 0:
                print("Unsafe packages listed which are not installed:")
                for unnecessary_unsafe_package in unnecessary_unsafe_packages:
                    print(f"  {unnecessary_unsafe_package}")

            if len(bad_unsafe_packages) > 0:
                print("Found unsafe packages with a known license. Instead allow these licenses explicitly:")
                for bad_package in bad_unsafe_packages:
                    print(f"  {bad_package['package']} ({bad_package['version']}): {bad_package['license']}")

            if len(missing_unsafe_packages) > 0:
                print("Found unsafe packages:")
                for missing_unsafe_package in missing_unsafe_packages:
                    print(f"  {missing_unsafe_package['package']} ({missing_unsafe_package['version']})")

            if len(unsafe_licenses) > 0:
                print("Found unsafe licenses:")
                for bad_license in unsafe_licenses:
                    print(f"  {bad_license['package']} ({bad_license['version']}): {bad_license['license']}")

            return 1

        print("All licenses ok")
        return 0
