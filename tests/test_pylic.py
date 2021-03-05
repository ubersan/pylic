import pytest
from pylic.pylic import read_license_from_classifier, read_licenses_from_metadata, read_pyproject_file
from pytest_mock import MockerFixture
from toml import TomlDecodeError


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


def test_reading_from_classifier_yields_correct_license(mocker: MockerFixture):
    distribution = mocker.MagicMock()
    expected_license = "pylic license"
    distribution.metadata = {"Classifier": f"License :: {expected_license}"}
    license = read_license_from_classifier(distribution)
    assert license == expected_license


def test_reading_from_classifier_with_no_classifier_yields_unknown_license(mocker: MockerFixture):
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 4 - Beta"}
    license = read_license_from_classifier(distribution)
    assert license == "unknown"


def test_reading_license_from_metadata_yields_correct_license(mocker: MockerFixture):
    distribution = mocker.MagicMock()
    expected_license = "uber license"
    distribution.metadata = {"License": expected_license}
    license = read_licenses_from_metadata(distribution)
    assert license == expected_license


def test_reading_license_from_metadata_without_license_entry_yields_unknown_license(mocker: MockerFixture):
    distribution = mocker.MagicMock()
    distribution.metadata = {"Classifier": "Development Status :: 3 - Alpha"}
    license = read_licenses_from_metadata(distribution)
    assert license == "unknown"


# def test_read_installed_license_metadata(mocker: MockerFixture):
#    mock = mocker.patch("pylic.pylic.distributions")
#    mock.return_value = 313
#    installed_licenses = read_installed_license_metadata()
#    assert installed_licenses == 3
