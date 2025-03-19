import typer

from pylic.__version__ import version as __version
from pylic.config import read_config
from pylic.license_checker import LicenseChecker
from pylic.licenses import read_all_installed_packages_metadata

app = typer.Typer(name="pylic")


@app.command(help="Checks all installed licenses against the configuaration provided in [tool.pylic].")
def check(
    quiet: bool = typer.Option(False, "--quiet", help="Only show warnings and errors."),
    allow_extra_unsafe_packages: bool = typer.Option(
        False, "--allow-extra-unsafe-packages", help="Allow to list extra unsafe packages."
    ),
    allow_extra_safe_licenses: bool = typer.Option(
        False, "--allow-extra-safe-licenses", help="Allow extra safe licenses."
    ),
) -> None:
    config = read_config()
    installed_licenses = read_all_installed_packages_metadata()
    checker = LicenseChecker(config, installed_licenses)
    error = False

    unnecessary_safe_licenses = checker.get_unnecessary_safe_licenses()
    if len(unnecessary_safe_licenses) > 0:
        error |= not allow_extra_safe_licenses
        print("Safe licenses listed which are not used by any installed package:")
        for unnecessary_safe_license in unnecessary_safe_licenses:
            print(f"  {unnecessary_safe_license}")

    unnecessary_unsafe_packages = checker.get_unnecessary_unsafe_packages()
    if len(unnecessary_unsafe_packages) > 0:
        error |= not allow_extra_unsafe_packages

        print("Unsafe packages listed which are not installed:")
        for unnecessary_unsafe_package in unnecessary_unsafe_packages:
            print(f"  {unnecessary_unsafe_package}")

    unsafe_package_names_with_safe_license = checker.get_unsafe_package_names_with_safe_license()
    if len(unsafe_package_names_with_safe_license) > 0:
        error = True
        print("Unsafe packages listed that have a safe license:")
        for unsafe_package_name_with_safe_license in unsafe_package_names_with_safe_license:
            print(f"  {unsafe_package_name_with_safe_license}")

    packages_with_unsafe_licenses = checker.get_packages_without_safe_license()
    if len(packages_with_unsafe_licenses) > 0:
        error = True
        print("Found installed packages with unsafe licenses:")
        for package in packages_with_unsafe_licenses:
            print(f"  {package.name} ({package.version}): {','.join(package.licenses)}")

    missing_unsafe_packages = checker.get_missing_unsafe_packages()
    if len(missing_unsafe_packages) > 0:
        error = True
        print("Found packages with unknown license, mark them as unsafe:")
        for package in missing_unsafe_packages:
            print(f"  {package.name} ({package.version})")

    if error:
        raise typer.Exit(1)

    if not quiet:
        print("✨ All licenses ok ✨")


@app.command(help="Lists all installed packages and their corresponding license.")
def list() -> None:
    installed_licenses = read_all_installed_packages_metadata()
    unsorted = {
        installed.name: {"version": installed.version, "license": ",".join(installed.licenses)}
        for installed in installed_licenses
    }
    for package, rest in sorted(unsorted.items(), key=lambda k: k[0].lower()):  # type:ignore
        print(f"{package} ({rest['version']}): {rest['license']}")


@app.command(help="Prints the version of pylic.")
def version() -> None:
    print(__version)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
