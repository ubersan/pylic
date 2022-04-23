import pytest
from toml import TomlDecodeError

from pylic.toml import read_config


def test_correct_exception_raised_if_toml_file_not_found() -> None:
    with pytest.raises(FileNotFoundError) as exception:
        read_config("does_not_exist.toml")

    assert exception.value.strerror == "No such file or directory"


def test_correct_exception_raised_if_toml_file_contains_invalid_content() -> None:
    with pytest.raises(TomlDecodeError):
        read_config("tests/unit_tests/test_tomls/invalid.toml")


def test_no_licenses_safe_if_no_pylic_tool_section_in_toml_file_found() -> None:
    safe_licenses, _ = read_config("tests/unit_tests/test_tomls/empty.toml")
    assert len(safe_licenses) == 0


def test_no_packages_unsafe_if_no_pylic_tool_section_in_toml_file_found() -> None:
    _, unsafe_packages = read_config("tests/unit_tests/test_tomls/empty.toml")
    assert len(unsafe_packages) == 0


def test_unknown_license_can_not_be_safe() -> None:
    with pytest.raises(ValueError) as exception:
        read_config("tests/unit_tests/test_tomls/unknown_license_allowed.toml")

    assert exception.value.args[0] == "'unknown' can't be an safe license. Whitelist the corresponding packages instead."
