# syntax=docker/dockerfile:1
#
# Two stages: build the environment, then copy only what runs.
# The uv binary is copied from its own published image rather than installed with
# a shell script, so the version is pinned by digest resolution and no network
# install happens at build time. Pattern taken from
# fastapi/full-stack-fastapi-template; the flags are documented at
# https://docs.astral.sh/uv/guides/integration/docker/

FROM python:3.14-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:0.11.16 /uv /uvx /bin/

# Bytecode is compiled at build time so the first request does not pay for it;
# copy mode avoids hardlinks that do not survive the stage boundary.
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependencies resolve from the lockfile alone, before any source is copied, so
# editing source does not invalidate this layer. --locked fails on a stale lock
# rather than quietly resolving something else.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev


FROM python:3.14-slim-bookworm AS runtime

# Runs unprivileged. A tool the agent can be argued into calling runs as this
# user, so the user is the blast radius.
RUN groupadd --gid 1001 app && useradd --uid 1001 --gid 1001 --no-create-home app

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
USER app

CMD ["python", "-m", "_your_product_.cli"]
