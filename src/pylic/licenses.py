from dataclasses import dataclass
from importlib.metadata import Distribution, distributions

from license_expression import ExpressionError, ExpressionParseError, get_spdx_licensing  # type: ignore[import-untyped]

spdx = get_spdx_licensing()


@dataclass
class Package:
    name: str
    licenses: list[str]
    version: str


def read_all_installed_packages_metadata() -> list[Package]:
    installed_packages: list[Package] = []

    for distribution in distributions():
        licenses = _read_license_expression_from_metadata(distribution)

        if len(licenses) == 1:
            license_string = licenses[0]

            if license_string == "unknown":
                license_string = _read_license_from_classifier(distribution)
            if license_string == "unknown":
                license_string = _read_license_from_metadata(distribution)
            if license_string == "OSI Approved":
                license_string = _read_license_from_metadata(distribution, fallback="OSI Approved")

            licenses = [license_string]

        installed_packages.append(
            Package(
                licenses=licenses,
                name=distribution.metadata["Name"],
                version=distribution.metadata["Version"],
            )
        )

    return installed_packages


def _read_license_from_classifier(distribution: Distribution) -> str:
    for key, content in distribution.metadata.items():  # type: ignore[attr-defined]
        if key == "Classifier":
            parts = [part.strip() for part in content.split("::")]
            if parts[0] == "License":
                return parts[-1]

    return "unknown"


def _read_license_from_metadata(distribution: Distribution, fallback: str = "unknown") -> str:
    return distribution.metadata.get("License", fallback)


def _read_license_expression_from_metadata(distribution: Distribution, fallback: str = "unknown") -> list[str]:
    expr = distribution.metadata.get("License-Expression")
    if expr is None:
        return [fallback]

    try:
        parsed = spdx.parse(expr, validate=True)
        return [str(symbol) for symbol in sorted(parsed.symbols)]
    except (ExpressionError, ExpressionParseError):
        pass

    return [expr]
