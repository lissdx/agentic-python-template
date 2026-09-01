# Single entry point for every command in this project.
# Nothing here needs an activated virtualenv: uv resolves the environment itself.
# `check` is the CI order, so a green terminal means a green pipeline.

.DEFAULT_GOAL := help
.PHONY: help install lint format format-check typecheck test notebooks notebooks-clean \
        check up down logs compose-check image rename clean

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

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

notebooks:  ## Fail if an experiment notebook carries outputs
	uv run python scripts/check_notebook_outputs.py

notebooks-clean:  ## Strip outputs from experiment notebooks, in place
	uv run python scripts/check_notebook_outputs.py --fix

check: lint format-check typecheck test notebooks  ## Everything CI gates on, in CI order

# The local stack lives under devenv/, so every invocation says where to look.
# --project-directory pins relative paths and .env to the repository root; without
# it Compose would resolve both against devenv/docker/.
COMPOSE = docker compose --project-directory . \
          -f devenv/docker/compose.yaml -f devenv/docker/compose.override.yaml

up:  ## Start the local stack; add SERVICES="db" for just one
	$(COMPOSE) up -d $(SERVICES)

down:  ## Stop the local stack; add VOLUMES=1 to discard its data
	$(COMPOSE) down $(if $(VOLUMES),--volumes,)

logs:  ## Follow the local stack's logs
	$(COMPOSE) logs -f

compose-check:  ## Validate the local stack definition without starting anything
	$(COMPOSE) config --quiet

image:  ## Build the container image and prove it runs
	docker build -f docker/Dockerfile -t agent-template:dev .
	docker run --rm agent-template:dev

# >>> template-only: this target and its script delete themselves on first use.
rename:  ## Turn the template into a project: make rename NAME=my-project [DROP_OPTIONAL=1]
	@test -n "$(NAME)" || { echo "NAME is required, e.g. make rename NAME=my-project"; exit 1; }
	uv run python scripts/rename_package.py --name "$(NAME)" $(if $(DROP_OPTIONAL),--drop-optional,)
	uv lock
# <<< template-only

clean:  ## Remove caches and build artifacts
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info
