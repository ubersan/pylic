from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import toml


@dataclass
class Config:
    safe_licenses: list[str] = field(default_factory=list)
    unsafe_packages: list[str] = field(default_factory=list)


def read_config(filename: str = "pyproject.toml") -> Config:
    project_config = _read_pyproject_file(filename)
    pylic_config = project_config.get("tool", {}).get("pylic", {})

    safe_licenses: list[str] = pylic_config.get("safe_licenses", [])
    if "unknown" in [safe_license.lower() for safe_license in safe_licenses]:
        raise ValueError(
            "'unknown' can't be a safe license, instead list the corresponding packages under 'unsafe_packages'."
        )

    unsafe_packages: list[str] = pylic_config.get("unsafe_packages", [])

    return Config(safe_licenses=safe_licenses, unsafe_packages=unsafe_packages)


def _read_pyproject_file(filename: str) -> dict[str, Any]:
    with Path.open(Path(filename)) as pyproject_file:
        try:
            return toml.load(pyproject_file)
        except Exception as exception:
            raise exception
