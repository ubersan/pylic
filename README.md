# pylic - Python license checker [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/sandrochuber/pylic/blob/main/LICENSE) [![PyPI version](https://badge.fury.io/py/pylic.svg)](https://badge.fury.io/py/pylic/)

A Python license checker. `pylic` is [PEP-639](https://peps.python.org/pep-0639/)-compliant and supports the [SPDX License Expression syntax](https://peps.python.org/pep-0639/#spdx-license-expression-syntax).

## Principles:

- All licenses of all installed packages are relevant.
- All installed packages without a license are considered unsafe and have to be listed as such.
- Every license has to be allowed explicitly.

## Installation

```sh
pip install pylic
```

## Configuration

`pylic` needs be run in the directory where your `pyproject.toml` file is located. You can configure

- `safe_licenses`: All licenses you consider safe for usage. The string comparison is case-insensitive.
- `unsafe_packages`: List packages that have no license or use licenses not considered safe.

```toml
[tool.pylic]
safe_licenses = [
    "Apache Software License",
    "Apache License 2.0",
    "MIT License",
    "Python Software Foundation License",
    "Mozilla Public License 2.0 (MPL 2.0)",
]
unsafe_packages = [
    "unsafe_package",
]
```

## Commands

`pylic` provides the following commands (also see `pylic --help`):

- `check`: Checks all installed licenses.
- `list`: Lists all installed packages and their corresponding license.

## Usage Example

Create a venv to start with a clean ground and activate it

```sh
python -m venv .venv
source .venv/bin/activate
```

Install `pylic` and create an empty `pyproject.toml`

```sh
pip install pylic
touch pyproject.toml
```

Install all your dependencies

```sh
pip install <packageA> <packageB>
```

Run pylic

```sh
pylic check
```

The output will be similar to

```sh
Found unsafe packages:
  pkg_resources (0.0.0)
Found unsafe licenses:
  pip (18.1): MIT License
  zipp (3.4.1): MIT License
  toml (0.10.2): MIT License
  pylic (1.2.0): MIT License
  setuptools (40.8.0): MIT License
  typing-extensions (3.7.4.3): Python Software Foundation License
  importlib-metadata (3.9.0): Apache Software License
```

The return code of `pylic` is in this case non-zero due to unsafe licenses. This allows usage of pylic in CI.

```sh
echo $? # prints 1
```

As these licenses and packages are all ok we can configure `pylic` accordingly

```sh
cat <<EOT >> pyproject.toml
[tool.pylic]
safe_licenses = ["Apache Software License", "MIT License", "Python Software Foundation License"]
unlicensed_packages = ["pkg_resources"]
EOT
```

After rerunning `pylic check` the output now reveals a successful validation

```sh
✨ All licenses ok ✨
```

Also the return code now signals that all is good

```sh
echo $? # prints 0
```

Use `pylic list` to list all installed packages and their corresponding licenses.

## Advanced Usage

In cases where the safe licenses or unsafe packages are centrally managed keeping the configuration in perfect sync to the installed packages might be too cumbersome or even impossible. To support these use cases the `check` command provides the two options (see also `check --help`) `--allow-extra-safe-licenses` and `--allow-extra-unsafe-packages`. These options only affect the returned status code and will keep all corresponding warnings unchanged.

## Pre-commit

`pylic` provides a [pre-commit](https://pre-commit.com/) integration. Follow the [instructions](https://pre-commit.com/#quick-start) and enable automatic license checking on commits by adding

```sh
-  repo: https://github.com/ubersan/pylic
   rev: v<version>
   hooks:
   -  id: pylic
```

to your `.pre-commit-config.yaml` file.

## Development

Required tools:

- uv (https://docs.astral.sh/uv/)

Run `uv sync` to install all necessary dependencies. Checkout the `[tool.taskipy.tasks]` (see [taskipy](https://github.com/illBeRoy/taskipy)) section in the `pyproject.toml` file for utility tasks. You can run these with `uv run task <task>`.

Creating a new release is as simple as:

- Update `version` in the pyproject.toml and the `__version__.py` file.
- Run `git tag <new-version>`.
- Run `git push origin <new-version>`.
