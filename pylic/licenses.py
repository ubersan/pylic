import sys
from typing import Dict, List

if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
    from importlib.metadata import Distribution, distributions
else:
    from importlib_metadata import Distribution, distributions


def read_all_installed_licenses_metadata() -> List[Dict]:
    installed_distributions = distributions()

    installed_licenses: List[Dict] = []
    for distribution in installed_distributions:
        license_string = _read_license_from_classifier(distribution)
        if license_string == "unknown":
            license_string = _read_license_from_metadata(distribution)
        if license_string == "OSI Approved":
            license_string = _read_license_from_metadata(distribution, fallback="OSI Approved")

        installed_licenses.append(
            {
                "license": license_string,
                "package": distribution.metadata["Name"],
                "version": distribution.metadata["Version"],
            }
        )

    return installed_licenses


def _read_license_from_classifier(distribution: Distribution) -> str:
    for key, content in distribution.metadata.items():
        if key == "Classifier":
            parts = [part.strip() for part in content.split("::")]
            if parts[0] == "License":
                return parts[-1]  # type: ignore[no-any-return]

    return "unknown"


def _read_license_from_metadata(distribution: Distribution, fallback: str = "unknown") -> str:
    return distribution.metadata.get("License", fallback)
