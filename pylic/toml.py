from typing import Any, List, MutableMapping, Tuple, cast

import toml


def read_pyproject_file() -> MutableMapping[str, Any]:
    with open("pyproject.toml", "r") as pyproject_file:
        try:
            return toml.load(pyproject_file)
        except Exception as exception:
            raise exception


def read_config() -> Tuple[List[str], List[str]]:
    project_config = read_pyproject_file()
    pylic_config = project_config.get("tool", {}).get("pylic", {})
    safe_licenses: List[str] = pylic_config.get("safe_licenses", [])

    if "unknown" in [safe_license.lower() for safe_license in safe_licenses]:
        raise ValueError("'unknown' can't be an safe license. Whitelist the corresponding packages instead.")

    unsafe_packages: List[str] = pylic_config.get("unsafe_packages", [])

    return (safe_licenses, unsafe_packages)


def read_version() -> str:
    project_config = read_pyproject_file()
    poetry_config = project_config.get("tool", {}).get("poetry", {})
    return cast(str, poetry_config["version"])


version = read_version()
