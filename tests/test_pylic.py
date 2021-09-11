import random
import string

import pytest
from pytest_mock import MockerFixture
from toml import TomlDecodeError

from pylic.pylic import (
    check_for_unnecessary_safe_licenses,
    check_for_unnecessary_unsafe_packages,
    check_licenses,
    check_unsafe_packages,
    main,
    read_all_installed_licenses_metadata,
    read_license_from_classifier,
    read_license_from_metadata,
    read_pyproject_file,
)


def random_string() -> str:
    return "".join(random.choice(string.ascii_lowercase) for i in range(10))


@pytest.fixture
def license() -> str:
    return random_string()


@pytest.fixture
def package() -> str:
    return random_string()


@pytest.fixture
def version() -> str:
    def random_integer() -> int:
        return random.randint(0, 100)

    return f"{random_integer()}.{random_integer()}.{random_integer()}"


def test_no_unncessary_licenses_found_if_no_safe_nor_installed_licenses_present(mocker: MockerFixture) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_licenses = check_for_unnecessary_safe_licenses(safe_licenses=[], installed_licenses=[])
    assert no_unncessary_licenses
    print_mock.assert_not_called()


def test_no_unncessary_licenses_found_if_no_safe_licenses_provided(mocker: MockerFixture, license: str) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_licenses = check_for_unnecessary_safe_licenses(
        safe_licenses=[], installed_licenses=[{"license": f"{license}1"}, {"license": f"{license}2"}]
    )
    assert no_unncessary_licenses
    print_mock.assert_not_called()


def test_all_licenses_unnecessary_if_no_installed_licenses_found(mocker: MockerFixture, license: str) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_licenses = check_for_unnecessary_safe_licenses(
        safe_licenses=[f"{license}1", f"{license}2", f"{license}3"], installed_licenses=[]
    )
    assert not no_unncessary_licenses
    assert print_mock.call_count == 4


def test_correct_unnecessary_safe_licenses_found(mocker: MockerFixture, license: str) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_licenses = check_for_unnecessary_safe_licenses(
        safe_licenses=[f"{license}2", f"{license}3"],
        installed_licenses=[{"license": f"{license}1"}, {"license": f"{license}2"}],
    )
    assert not no_unncessary_licenses
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {license}3"


def test_no_unncessary_packages_found_if_no_unsafe_nor_installed_packages_present(mocker: MockerFixture) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_packages = check_for_unnecessary_unsafe_packages(unsafe_packages=[], installed_licenses=[])
    assert no_unncessary_packages
    print_mock.assert_not_called()


def test_no_unncessary_packages_found_if_no_unsafe_packages_provided(mocker: MockerFixture, package: str) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_packages = check_for_unnecessary_unsafe_packages(
        unsafe_packages=[], installed_licenses=[{"package": f"{package}1"}, {"package": f"{package}2"}]
    )
    assert no_unncessary_packages
    print_mock.assert_not_called()


def test_all_packages_unnecessary_if_no_installed_packages_found(mocker: MockerFixture, package: str) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_packages = check_for_unnecessary_unsafe_packages(
        unsafe_packages=[f"{package}1", f"{package}2", f"{package}3"], installed_licenses=[]
    )
    assert not no_unncessary_packages
    assert print_mock.call_count == 4


def test_correct_unnecessary_unsafe_packages_found(mocker: MockerFixture, package: str) -> None:
    print_mock = mocker.patch("builtins.print")
    no_unncessary_packages = check_for_unnecessary_unsafe_packages(
        unsafe_packages=[f"{package}2", f"{package}3"],
        installed_licenses=[{"package": f"{package}1"}, {"package": f"{package}2"}],
    )
    assert not no_unncessary_packages
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {package}3"


def test_all_whitlisted_packages_valid_if_no_unsafe_packages_nor_any_packages_installed(mocker: MockerFixture) -> None:
    print_mock = mocker.patch("builtins.print")
    packages_valid = check_unsafe_packages([], [])
    assert packages_valid
    assert print_mock.call_count == 0


def test_unsafe_packages_invalid_if_corresponding_license_not_unknown(
    mocker: MockerFixture, package: str, version: str
) -> None:
    print_mock = mocker.patch("builtins.print")
    packages_valied = check_unsafe_packages(
        [package], [{"license": "not_unknown", "package": package, "version": version}]
    )
    assert not packages_valied
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "Found unsafe packages with a known license. Instead allow these licenses explicitly:"


def test_unsafe_packages_valid_if_corresponding_licenses_are_unknown(mocker: MockerFixture, package: str) -> None:
    print_mock = mocker.patch("builtins.print")
    packages_valid = check_unsafe_packages([package], [{"license": "unknown", "package": package}])
    assert packages_valid
    assert print_mock.call_count == 0


def test_unsafe_packages_invalid_if_license_unknown_but_package_not_listed_as_unsafe(
    mocker: MockerFixture, package: str, version: str
) -> None:
    print_mock = mocker.patch("builtins.print")
    packages_valid = check_unsafe_packages([], [{"license": "unknown", "package": package, "version": version}])
    assert not packages_valid
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "Found unsafe packages:"


def test_all_licenses_ok_if_no_packages_installed_or_unsafe_and_no_liceses_safe() -> None:
    all_licenses_ok = check_licenses(safe_licenses=[], installed_licenses=[])
    assert all_licenses_ok


def test_all_licenses_ok_if_unknown_license_is_unsafe(package: str) -> None:
    all_licenses_ok = check_licenses(
        safe_licenses=[],
        installed_licenses=[{"license": "unknown", "package": package}],
    )
    assert all_licenses_ok


def test_all_licenses_ok_if_licenses_are_all_safe(package: str, license: str) -> None:
    all_licenses_ok = check_licenses(
        safe_licenses=[f"{license}1", f"{license}2"],
        installed_licenses=[
            {"license": f"{license}1", "package": package},
            {"license": f"{license}2", "package": package},
        ],
    )
    assert all_licenses_ok


def test_all_invalid_licenses_are_found(mocker: MockerFixture, package: str, license: str, version: str) -> None:
    print_mock = mocker.patch("builtins.print")
    all_licenses_ok = check_licenses(
        safe_licenses=[f"{license}2"],
        installed_licenses=[
            {"license": f"{license}1", "package": package, "version": f"{version}1"},
            {"license": f"{license}2", "package": package, "version": f"{version}2"},
            {"license": f"{license}3", "package": package, "version": f"{version}3"},
            {"license": f"{license}4", "package": package, "version": f"{version}4"},
        ],
    )
    assert not all_licenses_ok
    assert print_mock.call_count == 4
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {package} ({version}1): {license}1"
    args, _ = print_mock.call_args_list[2]
    assert args[0] == f"  {package} ({version}3): {license}3"
    args, _ = print_mock.call_args_list[3]
    assert args[0] == f"  {package} ({version}4): {license}4"


def test_main_prints_success_and_exits_with_return_value_0_in_good_case(
    mocker: MockerFixture, package: str, license: str
) -> None:
    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
    mock_read_pyproject_file.return_value = ([license], [package])
    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
    mock_read_installed_licenses.return_value = [
        {"license": license, "package": f"{package}1"},
        {"license": "unknown", "package": package},
    ]
    print_mock = mocker.patch("builtins.print")
    main()
    assert print_mock.call_count == 1
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "All licenses ok"


def test_main_prints_errors_and_exits_with_return_value_1_with_bad_unsafe_packages(
    mocker: MockerFixture, package: str, license: str, version: str
) -> None:
    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
    mock_read_pyproject_file.return_value = ([license, f"{license}_not_unknown"], [package])
    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
    mock_read_installed_licenses.return_value = [
        {"license": license, "package": f"{package}1", "version": f"{version}1"},
        {"license": f"{license}_not_unknown", "package": package, "version": f"{version}2"},
    ]
    print_mock = mocker.patch("builtins.print")
    sys_exit_mock = mocker.patch("sys.exit")
    main()
    assert sys_exit_mock.called
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "Found unsafe packages with a known license. Instead allow these licenses explicitly:"
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {package} ({version}2): {license}_not_unknown"


def test_main_prints_errors_and_exits_with_return_value_1_with_unsafe_licenses_are_installed(
    mocker: MockerFixture, package: str, license: str, version: str
) -> None:
    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
    mock_read_pyproject_file.return_value = ([license], [package])
    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
    mock_read_installed_licenses.return_value = [
        {"license": license, "package": f"{package}1", "version": f"{version}1"},
        {"license": "unknown", "package": package, "version": f"{version}2"},
        {"license": f"{license}2", "package": f"{package}2", "version": f"{version}3"},
    ]
    print_mock = mocker.patch("builtins.print")
    sys_exit_mock = mocker.patch("sys.exit")
    main()
    sys_exit_mock.assert_called_once()
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "Found unsafe licenses:"
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {package}2 ({version}3): {license}2"


def test_main_prints_errors_and_exits_with_return_value_1_with_unnecessary_unsafe_packages_listed(
    mocker: MockerFixture, package: str
) -> None:
    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
    mock_read_pyproject_file.return_value = ([], [package])
    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
    mock_read_installed_licenses.return_value = []
    print_mock = mocker.patch("builtins.print")
    sys_exit_mock = mocker.patch("sys.exit")
    main()
    sys_exit_mock.assert_called_once()
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "Unsafe packages listed which are not installed:"
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {package}"


def test_main_prints_errors_and_exits_with_return_value_1_with_unnecessary_safe_licenses_listed(
    mocker: MockerFixture, license: str
) -> None:
    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
    mock_read_pyproject_file.return_value = ([license], [])
    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
    mock_read_installed_licenses.return_value = []
    print_mock = mocker.patch("builtins.print")
    sys_exit_mock = mocker.patch("sys.exit")
    main()
    sys_exit_mock.assert_called_once()
    assert print_mock.call_count == 2
    args, _ = print_mock.call_args_list[0]
    assert args[0] == "Unncessary safe licenses listed which are not used any installed package:"
    args, _ = print_mock.call_args_list[1]
    assert args[0] == f"  {license}"
