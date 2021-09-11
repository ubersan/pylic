from typing import Any, List, MutableMapping, Tuple

import toml


def read_config(filename: str = "pyproject.toml") -> Tuple[List[str], List[str]]:
    project_config = _read_pyproject_file(filename)
    pylic_config = project_config.get("tool", {}).get("pylic", {})
    safe_licenses: List[str] = pylic_config.get("safe_licenses", [])

    if "unknown" in [safe_license.lower() for safe_license in safe_licenses]:
        raise ValueError("'unknown' can't be an safe license. Whitelist the corresponding packages instead.")

    unsafe_packages: List[str] = pylic_config.get("unsafe_packages", [])

    return (safe_licenses, unsafe_packages)


def _read_pyproject_file(filename: str) -> MutableMapping[str, Any]:
    with open(filename, "r") as pyproject_file:
        try:
            return toml.load(pyproject_file)
        except Exception as exception:
            raise exception
