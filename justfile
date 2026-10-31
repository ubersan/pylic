default:
    @just --list

check-format:
    @echo 'Checking formatting ...'
    uv run ruff format --diff --quiet .

check-lint:
    @echo 'Checking linting ...'
    uv run ruff check --quiet .

check-types:
    @echo 'Checking types ...'
    uv run ty check .

check-licenses:
    @echo 'Checking licenses ...'
    uv run python -m pylic check --quiet

check: check-format check-lint check-types check-licenses
    @echo '✅'

fix-format:
    @echo 'Fixing formatting ...'
    uv run ruff format .

fix-lint:
    @echo 'Fixing linting ...'
    uv run ruff check --fix .

fix: fix-format fix-lint

test:
    uv run pytest
