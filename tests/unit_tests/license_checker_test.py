from pylic.license_checker import LicenseChecker


def test_no_unncessary_licenses_found_if_no_safe_nor_installed_licenses_present() -> None:
    checker = LicenseChecker()
    unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
    assert len(unnecessary_safe_licenses) == 0


def test_no_unncessary_licenses_found_if_no_safe_licenses_provided(license: str) -> None:
    checker = LicenseChecker(
        installed_licenses=[{"license": f"{license}1"}, {"license": f"{license}2"}],
    )
    unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
    assert len(unnecessary_safe_licenses) == 0


def test_all_licenses_unnecessary_if_no_installed_licenses_found(license: str) -> None:
    safe_licenses = [f"{license}1", f"{license}2", f"{license}3"]
    checker = LicenseChecker(safe_licenses=safe_licenses)
    unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
    assert unnecessary_safe_licenses == safe_licenses


def test_correct_unnecessary_safe_licenses_found(license: str) -> None:
    safe_licenses = [f"{license}2", f"{license}3"]
    installed_licenses = [{"license": f"{license}1"}, {"license": f"{license}2"}]
    checker = LicenseChecker(safe_licenses=safe_licenses, installed_licenses=installed_licenses)
    unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
    assert len(unnecessary_safe_licenses) == 1
    assert unnecessary_safe_licenses == [f"{license}3"]


def test_no_unncessary_packages_found_if_no_unsafe_nor_installed_packages_present() -> None:
    checker = LicenseChecker()
    unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
    assert len(unnecessary_unsafe_packages) == 0


def test_no_unncessary_packages_found_if_no_unsafe_packages_provided(package: str) -> None:
    checker = LicenseChecker(installed_licenses=[{"package": f"{package}1"}, {"package": f"{package}2"}])
    unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
    assert len(unnecessary_unsafe_packages) == 0


def test_all_packages_unnecessary_if_no_installed_packages_found(package: str) -> None:
    unsafe_packages = [f"{package}1", f"{package}2", f"{package}3"]
    checker = LicenseChecker(unsafe_packages=unsafe_packages)
    unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
    assert unnecessary_unsafe_packages == unsafe_packages


def test_correct_unnecessary_unsafe_packages_found(package: str) -> None:
    unsafe_packages = [f"{package}2", f"{package}3"]
    installed_licenses = [{"package": f"{package}1"}, {"package": f"{package}2"}]
    checker = LicenseChecker(unsafe_packages=unsafe_packages, installed_licenses=installed_licenses)
    unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
    assert len(unnecessary_unsafe_packages) == 1
    assert unnecessary_unsafe_packages == [f"{package}3"]


def test_no_bad_unsafe_packages_if_no_unsafe_packages_are_provided_or_installed_packages_found() -> None:
    checker = LicenseChecker()
    bad_unsafe_packages = checker.get_bad_unsafe_packages()
    assert len(bad_unsafe_packages) == 0


def test_no_bad_unsafe_packages_if_no_unsafe_packages_are_provided(package: str, license: str) -> None:
    checker = LicenseChecker(
        installed_licenses=[
            {"package": f"{package}1", "license": f"{license}1"},
            {"package": f"{package}2", "license": f"{license}2"},
        ]
    )
    bad_unsafe_packages = checker.get_bad_unsafe_packages()
    assert len(bad_unsafe_packages) == 0


def test_no_bad_unsafe_packages_if_all_licenses_of_unsafe_packages_come_with_unknown_license(package: str, version: str) -> None:
    checker = LicenseChecker(
        unsafe_packages=[f"{package}1", f"{package}2"],
        installed_licenses=[
            {"package": f"{package}1", "license": "unknown"},
            {"package": f"{package}2", "license": "unknown"},
        ],
    )
    bad_unsafe_packages = checker.get_bad_unsafe_packages()
    assert len(bad_unsafe_packages) == 0


def test_correct_bad_unsafe_packages_found(package: str, version: str) -> None:
    known_license = {"package": f"{package}1", "license": "not-uknown", "version": version}
    checker = LicenseChecker(
        unsafe_packages=[f"{package}1", f"{package}2"],
        installed_licenses=[
            known_license,
            {"package": f"{package}2", "license": "unknown"},
        ],
    )
    bad_unsafe_packages = checker.get_bad_unsafe_packages()
    assert len(bad_unsafe_packages) == 1
    assert bad_unsafe_packages == [known_license]


def test_no_missing_unsafe_packages_if_no_unsafe_packages_are_provided_or_installed_packages_found() -> None:
    checker = LicenseChecker()
    missing_unsafe_packages = checker.get_missing_unsafe_packages()
    assert len(missing_unsafe_packages) == 0


def test_no_missing_unsafe_packages_if_corresponding_unsafe_packages_are_provided(package: str) -> None:
    checker = LicenseChecker(
        unsafe_packages=[f"{package}1", f"{package}2"],
        installed_licenses=[
            {"package": f"{package}1", "license": "unknown"},
            {"package": f"{package}2", "license": "unknown"},
        ],
    )
    missing_unsafe_packages = checker.get_missing_unsafe_packages()
    assert len(missing_unsafe_packages) == 0


def test_no_missing_unsafe_packages_if_unsafe_packages_are_missing_but_licenses_are_known(package: str) -> None:
    checker = LicenseChecker(
        installed_licenses=[
            {"package": f"{package}1", "license": "not-unknown"},
            {"package": f"{package}2", "license": "also-not-unknown"},
        ],
    )
    missing_unsafe_packages = checker.get_missing_unsafe_packages()
    assert len(missing_unsafe_packages) == 0


def test_correct_missing_unsafe_packages_found(package: str, version: str) -> None:
    checker = LicenseChecker(
        unsafe_packages=[f"{package}1", f"{package}3"],
        installed_licenses=[
            {"package": f"{package}1", "license": "not-unknown", "version": f"{version}1"},
            {"package": f"{package}2", "license": "unknown", "version": f"{version}2"},
            {"package": f"{package}3", "license": "unknown", "version": f"{version}3"},
        ],
    )
    missing_unsafe_packages = checker.get_missing_unsafe_packages()
    assert len(missing_unsafe_packages) == 1
    assert missing_unsafe_packages == [{"package": f"{package}2", "version": f"{version}2"}]


def test_all_licenses_are_valied_if_no_packages_installed() -> None:
    checker = LicenseChecker()
    unsafe_licenses = checker.get_unsafe_licenses()
    assert len(unsafe_licenses) == 0


def test_unknown_licenses_are_not_considered_unsafe_per_se(package: str) -> None:
    checker = LicenseChecker(installed_licenses=[{"license": "unknown", "package": package}])
    unsafe_licenses = checker.get_unsafe_licenses()
    assert len(unsafe_licenses) == 0


def test_all_licenses_are_valid_if_are_listed_as_safe(package: str, license: str) -> None:
    checker = LicenseChecker(
        safe_licenses=[f"{license}1", f"{license}2", f"{license}3"],
        installed_licenses=[
            {"license": f"{license}1", "package": f"{package}1"},
            {"license": f"{license}2", "package": f"{package}2"},
            {"license": f"{license}3", "package": f"{package}3"},
        ],
    )
    unsafe_licenses = checker.get_unsafe_licenses()
    assert len(unsafe_licenses) == 0


def test_correct_unsafe_licenses_are_found(package: str, license: str, version: str) -> None:
    bad_licenses = [
        {"license": f"{license}1", "package": package, "version": f"{version}1"},
        {"license": f"{license}3", "package": package, "version": f"{version}3"},
        {"license": f"{license}4", "package": package, "version": f"{version}4"},
    ]
    checker = LicenseChecker(
        safe_licenses=[f"{license}2"],
        installed_licenses=[
            *bad_licenses,
            {"license": f"{license}2", "package": package, "version": f"{version}2"},
        ],
    )
    unsafe_licenses = checker.get_unsafe_licenses()
    assert len(unsafe_licenses) == 3
    assert unsafe_licenses == bad_licenses
