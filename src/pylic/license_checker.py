from dataclasses import dataclass
from typing import Optional

from pylic.config import Config


@dataclass
class UnsafeLicenses:
    found: list[dict]
    ignored: list[dict]


class LicenseChecker:
    def __init__(self, config: Optional[Config] = None, installed_licenses: Optional[list[dict]] = None) -> None:
        self.config = config or Config()
        self.installed_licenses = installed_licenses or []

    def get_unnecessary_safe_licenses(self) -> list[str]:
        installed_license_names = [license_info["license"].lower() for license_info in self.installed_licenses]

        unnecessary_safe_licenses = []
        lower_safe_licenses = [safe_license.lower() for safe_license in self.config.safe_licenses]

        for index, safe_license in enumerate(lower_safe_licenses):
            if safe_license not in installed_license_names:
                unnecessary_safe_licenses.append(self.config.safe_licenses[index])

        return unnecessary_safe_licenses

    def get_unnecessary_unsafe_packages(self) -> list[str]:
        installed_package_names = [license_info["package"].lower() for license_info in self.installed_licenses]

        unnecessary_unsafe_packages = []
        lower_unsafe_packages = [unsafe_package.lower() for unsafe_package in self.config.unsafe_packages]

        for index, unsafe_package in enumerate(lower_unsafe_packages):
            if unsafe_package not in installed_package_names:
                unnecessary_unsafe_packages.append(self.config.unsafe_packages[index])

        return unnecessary_unsafe_packages

    def get_unnecessary_ignore_packages(self) -> list[str]:
        installed_package_names = [license_info["package"].lower() for license_info in self.installed_licenses]

        unnecessary_ignore_packages = []
        lower_ignore_packages = [ignore_package.lower() for ignore_package in self.config.ignore_packages]

        for index, ignore_package in enumerate(lower_ignore_packages):
            if ignore_package not in installed_package_names:
                unnecessary_ignore_packages.append(self.config.ignore_packages[index])

        return unnecessary_ignore_packages

    def get_bad_unsafe_packages(self) -> list[dict]:
        bad_unsafe_packages: list[dict] = []

        for license_info in self.installed_licenses:
            license = license_info["license"]
            package = license_info["package"]

            if package in self.config.unsafe_packages and license.lower() != "unknown":
                bad_unsafe_packages.append({"license": license, "package": package, "version": license_info["version"]})

        return bad_unsafe_packages

    def get_missing_unsafe_packages(self) -> list[dict]:
        missing_unsafe_packages: list[dict] = []

        for license_info in self.installed_licenses:
            license = license_info["license"]
            package = license_info["package"]

            if license.lower() == "unknown" and package not in self.config.unsafe_packages:
                missing_unsafe_packages.append({"package": package, "version": license_info["version"]})

        return missing_unsafe_packages

    def get_unsafe_licenses(self) -> UnsafeLicenses:
        found_licenses: list[dict] = []
        ignored_licenses: list[dict] = []

        lower_safe_licenses = [safe_license.lower() for safe_license in self.config.safe_licenses]

        for license_info in self.installed_licenses:
            license = license_info["license"]

            if license.lower() == "unknown" or license.lower() in lower_safe_licenses:
                continue

            datum = {"license": license, "package": license_info["package"], "version": license_info["version"]}
            if license_info["package"] in self.config.ignore_packages:
                ignored_licenses.append(datum)
            else:
                found_licenses.append(datum)

        return UnsafeLicenses(found=found_licenses, ignored=ignored_licenses)
