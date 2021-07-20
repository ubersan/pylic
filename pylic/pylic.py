import sys
from typing import List, Tuple

import toml

if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
    from importlib.metadata import Distribution, distributions
else:
    from importlib_metadata import Distribution, distributions


def read_pyproject_file(filepath: str = "pyproject.toml") -> Tuple[List[str], List[str]]:
    with open(filepath, "r") as pyproject_file:
        try:
            project_config = toml.load(pyproject_file)
        except Exception as exception:
            raise exception

    pylic_config = project_config.get("tool", {}).get("pylic", {})
    safe_licenses: List[str] = pylic_config.get("safe_licenses", [])

    if "unknown" in [safe_license.lower() for safe_license in safe_licenses]:
        raise ValueError("'unknown' can't be an safe license. Whitelist the corresponding packages instead.")

    unsafe_packages: List[str] = pylic_config.get("unsafe_packages", [])

    return (safe_licenses, unsafe_packages)


def read_license_from_classifier(distribution: Distribution) -> str:
    for key, content in distribution.metadata.items():
        if key == "Classifier":
            parts = [part.strip() for part in content.split("::")]
            if parts[0] == "License":
                return parts[-1]  # type: ignore[no-any-return]

    return "unknown"


def read_license_from_metadata(distribution: Distribution, fallback: str = "unknown") -> str:
    return distribution.metadata.get("License", fallback)


def read_all_installed_licenses_metadata() -> List[dict]:
    installed_distributions = distributions()

    installed_licenses: List[dict] = []
    for distribution in installed_distributions:
        license_string = read_license_from_classifier(distribution)
        if license_string == "unknown":
            license_string = read_license_from_metadata(distribution)
        if license_string == "OSI Approved":
            license_string = read_license_from_metadata(distribution, fallback="OSI Approved")

        installed_licenses.append(
            {
                "license": license_string,
                "package": distribution.metadata["Name"],
                "version": distribution.metadata["Version"],
            }
        )

    return installed_licenses


def check_for_unnecessary_safe_licenses(safe_licenses: List[str], installed_licenses: List[dict]) -> bool:
    installed_license_names = [license_info["license"].lower() for license_info in installed_licenses]

    unnecessary_safe_licenses = []
    lower_safe_licenses = [safe_license.lower() for safe_license in safe_licenses]

    for index, safe_license in enumerate(lower_safe_licenses):
        if safe_license not in installed_license_names:
            unnecessary_safe_licenses.append(safe_licenses[index])

    if len(unnecessary_safe_licenses) > 0:
        print("Unncessary safe licenses listed which are not used any installed package:")
        for unnecessary_safe_license in unnecessary_safe_licenses:
            print(f"  {unnecessary_safe_license}")
        return False

    return True


def check_for_unnecessary_unsafe_packages(unsafe_packages: List[str], installed_licenses: List[dict]) -> bool:
    installed_package_names = [license_info["package"].lower() for license_info in installed_licenses]

    unnecessary_unsafe_packages = []
    lower_unsafe_packages = [unsafe_package.lower() for unsafe_package in unsafe_packages]

    for index, unsafe_package in enumerate(lower_unsafe_packages):
        if unsafe_package not in installed_package_names:
            unnecessary_unsafe_packages.append(unsafe_packages[index])

    if len(unnecessary_unsafe_packages) > 0:
        print("Unsafe packages listed which are not installed:")
        for unnecessary_unsafe_package in unnecessary_unsafe_packages:
            print(f"  {unnecessary_unsafe_package}")
        return False

    return True


def check_unsafe_packages(unsafe_packages: List[str], licenses: List[dict]) -> bool:
    bad_unsafe_packages: List[dict] = []
    missing_unsafe_packages: List[dict] = []

    for license_info in licenses:
        license = license_info["license"]
        package = license_info["package"]

        if package in unsafe_packages and license.lower() != "unknown":
            bad_unsafe_packages.append({"license": license, "package": package, "version": license_info["version"]})
        elif license.lower() == "unknown" and package not in unsafe_packages:
            missing_unsafe_packages.append({"package": package, "version": license_info["version"]})

    success = True
    if len(bad_unsafe_packages) > 0:
        print("Found unsafe packages with a known license. Instead allow these licenses explicitly:")
        for bad_package in bad_unsafe_packages:
            print(f"  {bad_package['package']} ({bad_package['version']}): {bad_package['license']}")
        success = False

    if len(missing_unsafe_packages) > 0:
        print("Found unsafe packages:")
        for missing_unsafe_package in missing_unsafe_packages:
            print(f"  {missing_unsafe_package['package']} ({missing_unsafe_package['version']})")
        success = False

    return success


def check_licenses(safe_licenses: List[str], installed_licenses: List[dict]) -> bool:
    bad_licenses: List[dict] = []
    lower_safe_licenses = [safe_license.lower() for safe_license in safe_licenses]

    for license_info in installed_licenses:
        license = license_info["license"]

        if license.lower() == "unknown" or license.lower() in lower_safe_licenses:
            continue

        bad_licenses.append(
            {"license": license, "package": license_info["package"], "version": license_info["version"]}
        )

    if len(bad_licenses) > 0:
        print("Found unsafe licenses:")
        for bad_license in bad_licenses:
            print(f"  {bad_license['package']} ({bad_license['version']}): {bad_license['license']}")
        return False

    return True


def main() -> None:
    safe_licenses, unsafe_packages = read_pyproject_file()
    installed_licenses = read_all_installed_licenses_metadata()
    no_unnecessary_safe_licenses = check_for_unnecessary_safe_licenses(safe_licenses, installed_licenses)
    no_unncessary_unsafe_packages = check_for_unnecessary_unsafe_packages(unsafe_packages, installed_licenses)
    packages_ok = check_unsafe_packages(unsafe_packages, installed_licenses)
    licenses_ok = check_licenses(safe_licenses, installed_licenses)

    if all([no_unnecessary_safe_licenses, no_unncessary_unsafe_packages, packages_ok, licenses_ok]):
        print("All licenses ok")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
