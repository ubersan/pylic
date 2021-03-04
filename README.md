# pylic - A Python license checker [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/sandrochuber/pylic/blob/main/LICENSE) [![PyPI version](https://badge.fury.io/py/pylic.svg)](https://badge.fury.io/py/pylic/) [![Codecov](https://codecov.io/gh/sandrochuber/pylic//branch/main/graph/badge.svg)](https://codecov.io/gh/sandrochuber/pylic/)

Reads the pyproject.toml file and checks all installed licenses recursively.

Principles:
- Every license has to be allowed explicitly (case-insensitive comparison).
- Packages with `UNKNOWN` licenses have to be explicitly whitelisted. Packages with a known license cannot be whitelisted.

## Example Configuration

```pyproject.toml
[tool.pylic]
allowed_licenses = [
    'MIT',
    'BSD'
]
whitelisted_packages = [
    "packageWithUnknownLicense"
]
```

## Development

Required tools:
- Poetry (https://python-poetry.org/)
- GitHub cli (https://github.com/cli/cli)

Creating a new release is as simple as:
- Update `version` in the pyproject.toml file.
- `poetry run task release vx.x.x`.
