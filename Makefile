# Single entry point for every command in this project.
# Nothing here needs an activated virtualenv: uv resolves the environment itself.
# `check` is the CI order, so a green terminal means a green pipeline.

.DEFAULT_GOAL := help
.PHONY: help install lint format format-check typecheck test check rename clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

install:  ## Create/refresh the virtualenv from uv.lock
	uv sync

lint:  ## Lint (same check CI runs)
	uv run ruff check .

format:  ## Format the tree in place
	uv run ruff format .

format-check:  ## Fail if the tree is not formatted (this is what CI runs)
	uv run ruff format --check .

typecheck:  ## Type-check in strict mode
	uv run mypy

test:  ## Run the unit tests
	uv run pytest tests/unit

check: lint format-check typecheck test  ## Everything CI gates on, in CI order

# >>> template-only: this target and its script delete themselves on first use.
rename:  ## Turn the template into a project: make rename NAME=my-project
	@test -n "$(NAME)" || { echo "NAME is required, e.g. make rename NAME=my-project"; exit 1; }
	uv run python scripts/rename_package.py --name "$(NAME)"
	uv lock
# <<< template-only

clean:  ## Remove caches and build artifacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info
