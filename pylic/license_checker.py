from typing import Dict, List, Optional


class LicenseChecker:
    def __init__(
        self,
        safe_licenses: Optional[List[str]] = None,
        unsafe_packages: Optional[List[str]] = None,
        installed_licenses: Optional[List[Dict]] = None,
    ) -> None:
        self.safe_licenses = safe_licenses or []
        self.unsafe_packages = unsafe_packages or []
        self.installed_licenses = installed_licenses or []

    def get_unnecessary_safe_licenses(self) -> List[str]:
        installed_license_names = [license_info["license"].lower() for license_info in self.installed_licenses]

        unnecessary_safe_licenses = []
        lower_safe_licenses = [safe_license.lower() for safe_license in self.safe_licenses]

        for index, safe_license in enumerate(lower_safe_licenses):
            if safe_license not in installed_license_names:
                unnecessary_safe_licenses.append(self.safe_licenses[index])

        return unnecessary_safe_licenses

    def get_unnecessary_unsafe_packages(self) -> List[str]:
        installed_package_names = [license_info["package"].lower() for license_info in self.installed_licenses]

        unnecessary_unsafe_packages = []
        lower_unsafe_packages = [unsafe_package.lower() for unsafe_package in self.unsafe_packages]

        for index, unsafe_package in enumerate(lower_unsafe_packages):
            if unsafe_package not in installed_package_names:
                unnecessary_unsafe_packages.append(self.unsafe_packages[index])

        return unnecessary_unsafe_packages

    def get_bad_unsafe_packages(self) -> List[Dict]:
        bad_unsafe_packages: List[Dict] = []

        for license_info in self.installed_licenses:
            license = license_info["license"]
            package = license_info["package"]

            if package in self.unsafe_packages and license.lower() != "unknown":
                bad_unsafe_packages.append({"license": license, "package": package, "version": license_info["version"]})

        return bad_unsafe_packages

    def get_missing_unsafe_packages(self) -> List[Dict]:
        missing_unsafe_packages: List[Dict] = []

        for license_info in self.installed_licenses:
            license = license_info["license"]
            package = license_info["package"]

            if license.lower() == "unknown" and package not in self.unsafe_packages:
                missing_unsafe_packages.append({"package": package, "version": license_info["version"]})

        return missing_unsafe_packages

    def get_unsafe_licenses(self) -> List[Dict]:
        unsafe_licenses: List[Dict] = []
        lower_safe_licenses = [safe_license.lower() for safe_license in self.safe_licenses]

        for license_info in self.installed_licenses:
            license = license_info["license"]

            if license.lower() == "unknown" or license.lower() in lower_safe_licenses:
                continue

            unsafe_licenses.append(
                {"license": license, "package": license_info["package"], "version": license_info["version"]}
            )

        return unsafe_licenses
