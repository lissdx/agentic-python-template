# docker/

Supporting files the containers in `compose.yaml` need — and nothing else. No
image is defined here.

| Path | What it is |
|---|---|
| `postgres/init.sql` | runs once, on an empty data directory: extensions, roles, schemas |

## Where things live, and when that changes

- **The image this repository builds** is `Dockerfile` at the root. That is where
  `docker build .` looks by default; moving it here costs a `-f` flag on every
  invocation and in every CI action, forever, and buys a directory holding one
  file. **When a second image appears, both move into `docker/<name>/Dockerfile`**
  and the root goes back to being clean. Woodpecker keeps seven that way, n8n
  five; Grafana, Prometheus, Vault and Traefik each keep their single one at the
  root.
- **The local stack** is `compose.yaml` at the root, with `compose.override.yaml`
  merged over it automatically. **When a second stack appears** — a minimal one
  and a full one, or a cloud-emulation one — **both move into `devenv/<name>/`**,
  which is what Grafana does in `devenv/docker/blocks/`.

The rule under both: one of a thing lives where the tool looks for it by default;
several of a thing get a directory.
