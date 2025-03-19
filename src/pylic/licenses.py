from dataclasses import dataclass
from importlib.metadata import Distribution, distributions

from license_expression import get_spdx_licensing  # type: ignore[import-untyped]

spdx = get_spdx_licensing()


@dataclass
class Package:
    name: str
    license: str
    version: str


def read_all_installed_packages_metadata() -> list[Package]:
    installed_packages: list[Package] = []

    for distribution in distributions():
        license_string = _read_license_expression_from_metadata(distribution)

        if license_string == "unknown":
            license_string = _read_license_from_classifier(distribution)
        if license_string == "unknown":
            license_string = _read_license_from_metadata(distribution)
        if license_string == "OSI Approved":
            license_string = _read_license_from_metadata(distribution, fallback="OSI Approved")

        installed_packages.append(
            Package(
                license=license_string,
                name=distribution.metadata["Name"],
                version=distribution.metadata["Version"],
            )
        )

    return installed_packages


def _read_license_from_classifier(distribution: Distribution) -> str:
    for key, content in distribution.metadata.items():  # type:ignore
        if key == "Classifier":
            parts = [part.strip() for part in content.split("::")]
            if parts[0] == "License":
                return parts[-1]  # type: ignore[no-any-return]

    return "unknown"


def _read_license_from_metadata(distribution: Distribution, fallback: str = "unknown") -> str:
    return distribution.metadata.get("License", fallback)  # type:ignore[no-any-return,attr-defined]


def _read_license_expression_from_metadata(distribution: Distribution, fallback: str = "unknown") -> str:
    license = distribution.metadata.get("License-Expression", fallback)  # type:ignore[no-any-return,attr-defined]
    lics = spdx.license_symbols(license)
    return str(lics[0])
