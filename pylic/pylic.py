import sys
from typing import List, Tuple

import toml

if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
    from importlib.metadata import Distribution, distributions
else:
    from importlib_metadata import Distribution, distributions  # type: ignore


def read_pyproject_file(filepath: str = "pyproject.toml") -> Tuple[List[str], List[str]]:
    with open(filepath, "r") as pyproject_file:
        try:
            project_config = toml.load(pyproject_file)
        except Exception as exception:
            raise exception

    pylic_config = project_config.get("tool", {}).get("pylic", {})
    allowed_licenses: List[str] = pylic_config.get("allowed_licenses", [])

    if "unknown" in [allowed_license.lower() for allowed_license in allowed_licenses]:
        raise ValueError("'unknown' can't be an allowed license. Whitelist the corresponding packages instead.")

    whitelisted_packages: List[str] = pylic_config.get("whitelisted_packages", [])

    return (allowed_licenses, whitelisted_packages)


def read_license_from_classifier(distribution: Distribution) -> str:
    for key, content in distribution.metadata.items():
        if key == "Classifier":
            parts = [part.strip() for part in content.split("::")]
            if parts[0] == "License":
                return parts[-1]

    return "unknown"


def read_licenses_from_metadata(distribution: Distribution) -> str:
    return distribution.metadata.get("License", "unknown")


def read_installed_license_metadata() -> List[dict]:
    installed_distributions = distributions()

    installed_licenses: List[dict] = []
    for distribution in installed_distributions:
        package_name = distribution.metadata["Name"]

        license_string = read_license_from_classifier(distribution)
        if license_string == "unknown":
            license_string = read_licenses_from_metadata(distribution)

        new_license = {"license": license_string, "package": package_name}
        installed_licenses.append(new_license)

    return installed_licenses


def check_whitelisted_packages(whitelisted_packages: List[str], licenses: List[dict]) -> bool:
    bad_whitelisted_packages: List[dict] = []
    for license_info in licenses:
        license = license_info["license"]
        package = license_info["package"]

        if package in whitelisted_packages and license.lower() != "unknown":
            bad_whitelisted_packages.append({"license": license, "package": package})

    if len(bad_whitelisted_packages) > 0:
        print("Found whitelisted packages with a known license. Instead allow these licenses explicitly:")
        for bad_package in bad_whitelisted_packages:
            print(f"\t{bad_package['package']}: {bad_package['license']}")
        return False

    return True


def check_licenses(
    allowed_licenses: List[str], whitelisted_packages: List[str], installed_licenses: List[dict]
) -> bool:
    bad_licenses: List[dict] = []
    lower_allowed_licenses = [allowed_license.lower() for allowed_license in allowed_licenses]

    for license_info in installed_licenses:
        license = license_info["license"]
        package = license_info["package"]

        if (
            license.lower() == "unknown" and package in whitelisted_packages
        ) or license.lower() in lower_allowed_licenses:
            continue

        bad_licenses.append({"license": license, "package": package})

    if len(bad_licenses) > 0:
        print("Found unallowed licenses:")
        for bad_license in bad_licenses:
            print(f"\t{bad_license['package']}: {bad_license['license']}")
        return False

    return True


def check_for_unnecessary_allowed_licenses(allowed_licenses: List[str], installed_licenses: List[dict]) -> None:
    installed_license_names = [license_info["license"].lower() for license_info in installed_licenses]

    unnecessary_allowed_licenses = []
    lower_allowed_licenses = [allowed_license.lower() for allowed_license in allowed_licenses]

    for index, allowed_license in enumerate(lower_allowed_licenses):
        if allowed_license not in installed_license_names:
            unnecessary_allowed_licenses.append(allowed_licenses[index])

    if len(unnecessary_allowed_licenses) > 0:
        print("Warning, found allowed licenses that are not used by any installed package:")
        for unnecessary_allowed_license in unnecessary_allowed_licenses:
            print(f"\t{unnecessary_allowed_license}")


def main():
    allowed_licenses, whitelisted_packages = read_pyproject_file()
    installed_licenses = read_installed_license_metadata()
    check_for_unnecessary_allowed_licenses(allowed_licenses, installed_licenses)
    packages_ok = check_whitelisted_packages(whitelisted_packages, installed_licenses)
    licenses_ok = check_licenses(allowed_licenses, whitelisted_packages, installed_licenses)

    if packages_ok and licenses_ok:
        print("All licenses ok")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
