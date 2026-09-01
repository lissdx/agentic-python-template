# docker/

The image this repository builds, and nothing that only runs on a developer's
machine — that half lives in [`devenv/`](../devenv/README.md).

```
docker/
├── Dockerfile                 two stages: build the environment, ship what runs
└── Dockerfile.dockerignore    the build context
```

## Two defaults this costs, both paid in the Makefile

Keeping the Dockerfile out of the repository root is a deliberate choice — the
count across forty-seven surveyed repositories is 24 root against 17 in a
directory. What it buys is a readable root. What it costs:

- `docker build .` looks for `Dockerfile` at the root of the context and does not
  find it, so every invocation needs `-f docker/Dockerfile`. `make image` carries
  it. **Do not call `docker build` here by hand.**
- The ignore-file cannot simply move with it: Docker reads `.dockerignore` from
  the root of the **build context**, which is the repository root. BuildKit adds
  the way out — *"Place your ignore-file in the same directory as the Dockerfile,
  and prefix the ignore-file with the name of the Dockerfile"*, and *"a
  Dockerfile-specific ignore-file takes precedence over the `.dockerignore` file
  at the root of the build context if both exist."* Hence
  `Dockerfile.dockerignore`. It requires BuildKit, the default builder since
  Docker 23.

## When a second image appears

Each gets its own subdirectory with its ignore-file beside it —
`docker/api/Dockerfile`, `docker/worker/Dockerfile`. That is the arrangement
Woodpecker uses for seven images and n8n for five.
