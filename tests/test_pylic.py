# import random
# import string
#
# import pytest
# from pytest_mock import MockerFixture
# from toml import TomlDecodeError
#
# from pylic.pylic import (
#    check_for_unnecessary_safe_licenses,
#    check_for_unnecessary_unsafe_packages,
#    check_licenses,
#    check_unsafe_packages,
#    main,
#    read_all_installed_licenses_metadata,
#    read_license_from_classifier,
#    read_license_from_metadata,
#    read_pyproject_file,
# )
#
#
# def random_string() -> str:
#    return "".join(random.choice(string.ascii_lowercase) for i in range(10))
#
#
# @pytest.fixture
# def license() -> str:
#    return random_string()
#
#
# @pytest.fixture
# def package() -> str:
#    return random_string()
#
#
# @pytest.fixture
# def version() -> str:
#    def random_integer() -> int:
#        return random.randint(0, 100)
#
#    return f"{random_integer()}.{random_integer()}.{random_integer()}"
#
#

#
#

#
#

#
#

#
#
# def test_main_prints_success_and_exits_with_return_value_0_in_good_case(
#    mocker: MockerFixture, package: str, license: str
# ) -> None:
#    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
#    mock_read_pyproject_file.return_value = ([license], [package])
#    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
#    mock_read_installed_licenses.return_value = [
#        {"license": license, "package": f"{package}1"},
#        {"license": "unknown", "package": package},
#    ]
#    print_mock = mocker.patch("builtins.print")
#    main()
#    assert print_mock.call_count == 1
#    args, _ = print_mock.call_args_list[0]
#    assert args[0] == "All licenses ok"
#
#
# def test_main_prints_errors_and_exits_with_return_value_1_with_bad_unsafe_packages(
#    mocker: MockerFixture, package: str, license: str, version: str
# ) -> None:
#    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
#    mock_read_pyproject_file.return_value = ([license, f"{license}_not_unknown"], [package])
#    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
#    mock_read_installed_licenses.return_value = [
#        {"license": license, "package": f"{package}1", "version": f"{version}1"},
#        {"license": f"{license}_not_unknown", "package": package, "version": f"{version}2"},
#    ]
#    print_mock = mocker.patch("builtins.print")
#    sys_exit_mock = mocker.patch("sys.exit")
#    main()
#    assert sys_exit_mock.called
#    assert print_mock.call_count == 2
#    args, _ = print_mock.call_args_list[0]
#    assert args[0] == "Found unsafe packages with a known license. Instead allow these licenses explicitly:"
#    args, _ = print_mock.call_args_list[1]
#    assert args[0] == f"  {package} ({version}2): {license}_not_unknown"
#
#
# def test_main_prints_errors_and_exits_with_return_value_1_with_unsafe_licenses_are_installed(
#    mocker: MockerFixture, package: str, license: str, version: str
# ) -> None:
#    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
#    mock_read_pyproject_file.return_value = ([license], [package])
#    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
#    mock_read_installed_licenses.return_value = [
#        {"license": license, "package": f"{package}1", "version": f"{version}1"},
#        {"license": "unknown", "package": package, "version": f"{version}2"},
#        {"license": f"{license}2", "package": f"{package}2", "version": f"{version}3"},
#    ]
#    print_mock = mocker.patch("builtins.print")
#    sys_exit_mock = mocker.patch("sys.exit")
#    main()
#    sys_exit_mock.assert_called_once()
#    assert print_mock.call_count == 2
#    args, _ = print_mock.call_args_list[0]
#    assert args[0] == "Found unsafe licenses:"
#    args, _ = print_mock.call_args_list[1]
#    assert args[0] == f"  {package}2 ({version}3): {license}2"
#
#
# def test_main_prints_errors_and_exits_with_return_value_1_with_unnecessary_unsafe_packages_listed(
#    mocker: MockerFixture, package: str
# ) -> None:
#    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
#    mock_read_pyproject_file.return_value = ([], [package])
#    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
#    mock_read_installed_licenses.return_value = []
#    print_mock = mocker.patch("builtins.print")
#    sys_exit_mock = mocker.patch("sys.exit")
#    main()
#    sys_exit_mock.assert_called_once()
#    assert print_mock.call_count == 2
#    args, _ = print_mock.call_args_list[0]
#    assert args[0] == "Unsafe packages listed which are not installed:"
#    args, _ = print_mock.call_args_list[1]
#    assert args[0] == f"  {package}"
#
#
# def test_main_prints_errors_and_exits_with_return_value_1_with_unnecessary_safe_licenses_listed(
#    mocker: MockerFixture, license: str
# ) -> None:
#    mock_read_pyproject_file = mocker.patch("pylic.pylic.read_pyproject_file")
#    mock_read_pyproject_file.return_value = ([license], [])
#    mock_read_installed_licenses = mocker.patch("pylic.pylic.read_all_installed_licenses_metadata")
#    mock_read_installed_licenses.return_value = []
#    print_mock = mocker.patch("builtins.print")
#    sys_exit_mock = mocker.patch("sys.exit")
#    main()
#    sys_exit_mock.assert_called_once()
#    assert print_mock.call_count == 2
#    args, _ = print_mock.call_args_list[0]
#    assert args[0] == "Unncessary safe licenses listed which are not used any installed package:"
#    args, _ = print_mock.call_args_list[1]
#    assert args[0] == f"  {license}"
#
