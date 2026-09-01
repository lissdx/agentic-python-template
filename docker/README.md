# docker/

Everything about containers lives here — the image, the local stack, and the
files those containers need. The repository root stays free of them.

```
docker/
├── Dockerfile                    the image this repository builds
├── Dockerfile.dockerignore       its build context; see the note below
├── devenv/
│   ├── compose.yaml              the local stack
│   └── compose.override.yaml     dev only: exposed port, bind mount, debug logs
└── postgres/
    └── init.sql                  runs once, on an empty data directory
```

## Use the Makefile, not the raw commands

Two things stop working the moment these files leave the root, and both are
handled once in the `Makefile` rather than remembered every time:

- `docker build .` no longer finds the Dockerfile — it needs
  `-f docker/Dockerfile`. `make image` carries it.
- Compose resolves relative paths **and reads `.env`** from its project
  directory, which defaults to the directory of the first `-f` file. Left alone
  it would look in `docker/devenv/`. `make up` passes `--project-directory .`,
  which pins both to the repository root — so every path inside `compose.yaml`
  is written the way a person reads it, from the root.

```
make up                  start everything      make up SERVICES=db   only the database
make down                stop                  make down VOLUMES=1   stop and discard data
make logs                follow the logs
make image               build the image and run it
```

## The ignore-file's name is not a typo

Docker looks for `.dockerignore` at the root of the **build context**, which is
the repository root — not next to the Dockerfile. BuildKit adds a second option:
*"Place your ignore-file in the same directory as the Dockerfile, and prefix the
ignore-file with the name of the Dockerfile"*, and *"a Dockerfile-specific
ignore-file takes precedence over the `.dockerignore` file at the root of the
build context if both exist."* That is why this one is `Dockerfile.dockerignore`
and lives here. It requires BuildKit, which has been the default builder since
Docker 23.

## When this grows

- **A second image** gets its own subdirectory: `docker/api/Dockerfile`,
  `docker/worker/Dockerfile`, each with its own ignore-file beside it.
- **A second local stack** gets its own subdirectory under `devenv/`:
  `docker/devenv/minimal/`, `docker/devenv/full/`, `docker/devenv/cloud/` — the
  shape Grafana uses in `devenv/docker/blocks/`.
