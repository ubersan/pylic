from pylic.config import Config
from pylic.licenses import Package


class LicenseChecker:
    def __init__(self, config: Config, installed_packages: list[Package]) -> None:
        self.config = config
        self.installed_packages = installed_packages

    def get_unnecessary_safe_licenses(self) -> list[str]:
        installed_license_names = [
            license.lower() for package in self.installed_packages for license in package.licenses
        ]
        return [
            safe_license
            for safe_license in self.config.safe_licenses
            if safe_license.lower() not in installed_license_names
        ]

    def get_unnecessary_unsafe_packages(self) -> list[str]:
        installed_package_names = [package.name for package in self.installed_packages]
        return [package for package in self.config.unsafe_packages if package not in installed_package_names]

    def get_unsafe_package_names_with_safe_license(self) -> list[str]:
        safe_license_names = [safe_license.lower() for safe_license in self.config.safe_licenses]
        safe_package_names = [
            package.name
            for package in self.installed_packages
            if {license.lower() for license in package.licenses}.issubset(set(safe_license_names))
        ]

        return [package_name for package_name in self.config.unsafe_packages if package_name in safe_package_names]

    def get_packages_without_safe_license(self) -> list[Package]:
        safe_license_names = [safe_license.lower() for safe_license in self.config.safe_licenses]
        return [
            package
            for package in self.installed_packages
            if (len(package.licenses) == 1 and package.licenses[0].lower() != "unknown")
            and not {license.lower() for license in package.licenses}.issubset(set(safe_license_names))
            and package.name not in self.config.unsafe_packages
        ]

    def get_missing_unsafe_packages(self) -> list[Package]:
        return [
            package
            for package in self.installed_packages
            if (len(package.licenses) == 1 and package.licenses[0].lower() == "unknown")
            and package.name not in self.config.unsafe_packages
        ]
