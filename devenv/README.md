# devenv/

The development environment: everything needed to run this project on your own
machine, and nothing that ships.

```
devenv/
└── docker/
    ├── compose.yaml              the local stack
    ├── compose.override.yaml     dev only: exposed port, bind mount, debug logs
    └── postgres/init.sql         runs once, on an empty data directory
```

**Docker is one mechanism here, not the organising idea.** A development
environment is also seed data, fixtures, a local cluster, a `direnv` file — none
of which are containers. So the concern owns the directory and the mechanism sits
inside it, which is the shape Grafana uses in `devenv/docker/blocks/`.

The split against [`docker/`](../docker/README.md) is the same rule the package
follows one level down: **what ships lives on one side, what only a developer
needs lives on the other.**

## Use the Makefile

Compose resolves relative paths **and reads `.env`** from its project directory,
which defaults to the directory of the first `-f` file — here that would be
`devenv/docker/`. `make up` passes `--project-directory .` and pins both to the
repository root, so every path inside `compose.yaml` is written the way a person
reads it. Calling `docker compose` by hand silently resolves them somewhere else.

```
make up                  start everything      make up SERVICES=db   only the database
make down                stop                  make down VOLUMES=1   stop and discard data
make logs                follow the logs
make compose-check       validate without starting anything
```

`compose.override.yaml` is merged over the base file; anything true only on a
developer's machine belongs there and nowhere else.

## When a second stack appears

Each gets its own subdirectory — `devenv/docker/minimal/`, `devenv/docker/full/`,
`devenv/docker/cloud/` for an emulated cloud — and `make up STACK=<name>` picks
one. Grafana keeps dozens that way, one per dependency.
