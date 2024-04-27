import random

import pytest
from pytest_mock import MockerFixture

from pylic.licenses import _read_license_from_classifier, _read_license_from_metadata, read_all_installed_licenses_metadata
from tests.unit_tests.conftest import random_string


@pytest.fixture
def package() -> str:
    return random_string()


@pytest.fixture
def version() -> str:
    def random_integer() -> int:
        return random.randint(0, 100)

    return f"{random_integer()}.{random_integer()}.{random_integer()}"


def test_reading_from_classifier_yields_correct_license(mocker: MockerFixture, license: str) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": f"License :: {license}"}
    read_license = _read_license_from_classifier(distribution)
    assert read_license == license


def test_reading_from_classifier_with_no_classifier_yields_unknown_license(mocker: MockerFixture) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 4 - Beta"}
    license = _read_license_from_classifier(distribution)
    assert license == "unknown"


def test_reading_license_from_metadata_yields_correct_license(mocker: MockerFixture, license: str) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"License": license}
    read_license = _read_license_from_metadata(distribution)
    assert read_license == license


def test_reading_license_from_metadata_without_license_entry_yields_unknown_license(mocker: MockerFixture) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 3 - Alpha"}
    read_license = _read_license_from_metadata(distribution)
    assert read_license == "unknown"


def test_reading_license_from_metadata_yields_provided_fallback_license_when_no_license_found(mocker: MockerFixture, license: str) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 3 - Alpha"}
    read_license = _read_license_from_metadata(distribution, fallback=license)
    assert read_license == license


def test_reading_all_installed_license_metadata_return_correct_result(
    mocker: MockerFixture, license: str, package: str, version: str
) -> None:
    distribution1 = mocker.MagicMock()
    distribution1.metadata = {
        "Classifier": f"License :: {license}1",
        "Name": f"{package}1",
        "License": "do_not_use_this1",
        "Version": f"{version}1",
    }
    distribution2 = mocker.MagicMock()
    distribution2.metadata = {
        "Classifier": f"License :: {license}2",
        "Name": f"{package}2",
        "License": "do_not_use_this2",
        "Version": f"{version}2",
    }

    mock = mocker.patch("pylic.licenses.distributions")
    mock.return_value = [distribution1, distribution2]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 2
    assert installed_licenses[0] == {"license": f"{license}1", "package": f"{package}1", "version": f"{version}1"}
    assert installed_licenses[1] == {"license": f"{license}2", "package": f"{package}2", "version": f"{version}2"}


def test_correct_license_metadata_is_returned_if_no_classifiers_are_present(
    mocker: MockerFixture, license: str, package: str, version: str
) -> None:
    distribution1 = mocker.MagicMock()
    distribution1.metadata = {"Name": f"{package}1", "License": f"{license}", "Version": f"{version}1"}
    distribution2 = mocker.MagicMock()
    distribution2.metadata = {"Name": f"{package}2", "Version": f"{version}2"}

    mock = mocker.patch("pylic.licenses.distributions")
    mock.return_value = [distribution1, distribution2]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 2
    assert installed_licenses[0] == {"license": f"{license}", "package": f"{package}1", "version": f"{version}1"}
    assert installed_licenses[1] == {"license": "unknown", "package": f"{package}2", "version": f"{version}2"}


def test_osi_approved_license_is_returned_if_osi_approved_classifier_and_no_specific_license_is_set(
    mocker: MockerFixture, license: str, package: str, version: str
) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "License :: OSI Approved", "Name": package, "Version": version}

    mock = mocker.patch("pylic.licenses.distributions")
    mock.return_value = [distribution]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 1
    assert installed_licenses[0] == {"license": "OSI Approved", "package": package, "version": version}


def test_specific_license_is_returned_if_only_general_osi_approved_classifier_is_set(
    mocker: MockerFixture, license: str, package: str, version: str
) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "License :: OSI Approved", "Name": package, "License": license, "Version": version}

    mock = mocker.patch("pylic.licenses.distributions")
    mock.return_value = [distribution]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 1
    assert installed_licenses[0] == {"license": license, "package": package, "version": version}


def test_the_specific_osi_approved_classifier_license_is_returned_even_when_and_a_specific_license_is_provided(
    mocker: MockerFixture, license: str, package: str, version: str
) -> None:
    distribution = mocker.MagicMock()
    distribution.metadata = {
        "Classifier": f"License :: OSI Approved :: {license}",
        "Name": package,
        "License": "do not use this",
        "Version": version,
    }

    mock = mocker.patch("pylic.licenses.distributions")
    mock.return_value = [distribution]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 1
    assert installed_licenses[0] == {"license": license, "package": package, "version": version}
