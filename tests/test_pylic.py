import pytest
from pylic.pylic import read_pyproject_file
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
