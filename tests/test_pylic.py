import random
import string

import pytest
from pylic.pylic import (
    check_for_unnecessary_allowed_licenses,
    check_for_unnecessary_whitelisted_packages,
    read_all_installed_licenses_metadata,
    read_license_from_classifier,
    read_license_from_metadata,
    read_pyproject_file,
)
from pytest_mock import MockerFixture
from toml import TomlDecodeError


def random_string():
    return "".join(random.choice(string.ascii_lowercase) for i in range(10))


@pytest.fixture
def license():
    return random_string()


@pytest.fixture
def package():
    return random_string()


def test_correct_exception_raised_if_toml_file_not_found():
    with pytest.raises(FileNotFoundError) as exception:
        read_pyproject_file("does_not_exist.toml")

    assert exception.value.strerror == "No such file or directory"


def test_correct_exception_raised_if_toml_file_contains_invalid_content():
    with pytest.raises(TomlDecodeError):
        read_pyproject_file("tests/test_tomls/invalid.toml")


def test_no_licenses_allowed_if_no_pylic_tool_section_in_toml_file_found():
    allowed_licenses, _ = read_pyproject_file("tests/test_tomls/empty.toml")
    assert len(allowed_licenses) == 0


def test_no_packages_whitelisted_if_no_pylic_tool_section_in_toml_file_found():
    _, whitelisted_packages = read_pyproject_file("tests/test_tomls/empty.toml")
    assert len(whitelisted_packages) == 0


def test_unknown_license_can_not_be_allowed():
    with pytest.raises(ValueError) as exception:
        read_pyproject_file("tests/test_tomls/unknown_license_allowed.toml")

    assert (
        exception.value.args[0]
        == "'unknown' can't be an allowed license. Whitelist the corresponding packages instead."
    )


def test_reading_from_classifier_yields_correct_license(mocker: MockerFixture, license: str):
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": f"License :: {license}"}
    read_license = read_license_from_classifier(distribution)
    assert read_license == license


def test_reading_from_classifier_with_no_classifier_yields_unknown_license(mocker: MockerFixture):
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 4 - Beta"}
    license = read_license_from_classifier(distribution)
    assert license == "unknown"


def test_reading_license_from_metadata_yields_correct_license(mocker: MockerFixture, license: str):
    distribution = mocker.MagicMock()
    distribution.metadata = {"License": license}
    read_license = read_license_from_metadata(distribution)
    assert read_license == license


def test_reading_license_from_metadata_without_license_entry_yields_unknown_license(mocker: MockerFixture):
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 3 - Alpha"}
    read_license = read_license_from_metadata(distribution)
    assert read_license == "unknown"


def test_reading_all_installed_license_metadata_return_correct_result(
    mocker: MockerFixture, license: str, package: str
):
    distribution1 = mocker.MagicMock()
    distribution1.metadata = {
        "Classifier": f"License :: {license}1",
        "Name": f"{package}1",
        "License": "do_not_use_this1",
    }
    distribution2 = mocker.MagicMock()
    distribution2.metadata = {
        "Classifier": f"License :: {license}2",
        "Name": f"{package}2",
        "License": "do_not_use_this2",
    }

    mock = mocker.patch("pylic.pylic.distributions")
    mock.return_value = [distribution1, distribution2]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 2
    assert installed_licenses[0] == {"license": f"{license}1", "package": f"{package}1"}
    assert installed_licenses[1] == {"license": f"{license}2", "package": f"{package}2"}


def test_correct_license_metadata_is_returned_if_no_classifiers_are_present(
    mocker: MockerFixture, license: str, package: str
):
    distribution1 = mocker.MagicMock()
    distribution1.metadata = {"Name": f"{package}1", "License": f"{license}"}
    distribution2 = mocker.MagicMock()
    distribution2.metadata = {"Name": f"{package}2"}

    mock = mocker.patch("pylic.pylic.distributions")
    mock.return_value = [distribution1, distribution2]
    installed_licenses = read_all_installed_licenses_metadata()

    assert len(installed_licenses) == 2
    assert installed_licenses[0] == {"license": f"{license}", "package": f"{package}1"}
    assert installed_licenses[1] == {"license": "unknown", "package": f"{package}2"}


def test_no_unncessary_licenses_found_if_no_allowed_nor_installed_licenses_present(mocker: MockerFixture):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_allowed_licenses(allowed_licenses=[], installed_licenses=[])
    print_mock.assert_not_called()


def test_no_unncessary_licenses_found_if_no_allowed_licenses_provided(mocker: MockerFixture, license: str):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_allowed_licenses(
        allowed_licenses=[], installed_licenses=[{"license": f"{license}1"}, {"license": f"{license}2"}]
    )
    print_mock.assert_not_called()


def test_all_licenses_unnecessary_if_no_installed_licenses_found(mocker: MockerFixture, license: str):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_allowed_licenses(
        allowed_licenses=[f"{license}1", f"{license}2", f"{license}3"], installed_licenses=[]
    )
    assert print_mock.call_count == 4


def test_correct_unnecessary_allowed_licenses_found(mocker: MockerFixture, license: str):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_allowed_licenses(
        allowed_licenses=[f"{license}2", f"{license}3"],
        installed_licenses=[{"license": f"{license}1"}, {"license": f"{license}2"}],
    )
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"\t{license}3"


def test_no_unncessary_packages_found_if_no_whitelisted_nor_installed_packages_present(mocker: MockerFixture):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_whitelisted_packages(whitelisted_packages=[], installed_licenses=[])
    print_mock.assert_not_called()


def test_no_unncessary_packages_found_if_no_whitelisted_packages_provided(mocker: MockerFixture, package: str):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_whitelisted_packages(
        whitelisted_packages=[], installed_licenses=[{"package": f"{package}1"}, {"package": f"{package}2"}]
    )
    print_mock.assert_not_called()


def test_all_packages_unnecessary_if_no_installed_packages_found(mocker: MockerFixture, package: str):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_whitelisted_packages(
        whitelisted_packages=[f"{package}1", f"{package}2", f"{package}3"], installed_licenses=[]
    )
    assert print_mock.call_count == 4


def test_correct_unnecessary_whitelisted_packages_found(mocker: MockerFixture, package: str):
    print_mock = mocker.patch("builtins.print")
    check_for_unnecessary_whitelisted_packages(
        whitelisted_packages=[f"{package}2", f"{package}3"],
        installed_licenses=[{"package": f"{package}1"}, {"package": f"{package}2"}],
    )
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"\t{package}3"
