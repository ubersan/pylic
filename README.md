# pylic - A Python license checker

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
