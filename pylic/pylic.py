import sys
from importlib import metadata
from typing import List, Tuple

import toml


def read_pyproject_file() -> Tuple[List[str], List[str]]:
    with open("pyproject.toml", "r") as pyproject_file:
        try:
            project_config = toml.load(pyproject_file)
        except Exception as exception:
            print("Could not load pyproject.toml file.")
            raise exception

    tool_config = project_config.get("tool", None)
    if tool_config is None:
        raise Exception("No 'tool' section found in the pyproject.toml file. Excpecting a [tool.pylic] section.")

    pylic_config = tool_config.get("pylic", None)
    if pylic_config is None:
        raise Exception("No 'tool.pylic' section found in the pyproject.toml file. Excpecting a [tool.pylic] section.")

    allowed_licenses: List[str] = pylic_config.get("allowed_licenses", [])
    whitelisted_packages: List[str] = pylic_config.get("whitelisted_packages", [])

    return (allowed_licenses, whitelisted_packages)


def read_installed_license_metadata() -> List[dict]:
    distributions = metadata.distributions()

    installed_licenses: List[dict] = []
    for distribution in distributions:
        package_name = distribution.metadata["Name"]
        licenses_string = distribution.metadata.get("License", "UNKNOWN")
        new_licenses = [
            {"license": license_name.strip(), "package": package_name} for license_name in licenses_string.split(",")
        ]
        installed_licenses += new_licenses

    return installed_licenses


def check_licenses(allowed_licenses: List[str], whitelisted_packages: List[str], licenses: List[dict]) -> None:
    bad_licenses: List[dict] = []
    for license_info in licenses:
        license = license_info["license"]
        package = license_info["package"]
        if license not in allowed_licenses and package not in whitelisted_packages:
            bad_licenses.append({"license": license, "package": package})

    if len(bad_licenses) > 0:
        print("Found bad licenses:")
        for license_info in bad_licenses:
            print(f"\t{license_info['package']}: {license_info['license']}")
        sys.exit(1)

    print("All licenses ok")


def main():
    allowed_licenses, whitelisted_packages = read_pyproject_file()
    installed_licenses = read_installed_license_metadata()
    check_licenses(allowed_licenses, whitelisted_packages, installed_licenses)


if __name__ == "__main__":
    main()
