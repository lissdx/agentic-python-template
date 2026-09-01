# Migrations

Schema history lives here, **outside** the package: migrations are executed by a
migration tool, not imported by the application, so they have no reason to ship
in the wheel.

Only five of the thirteen surveyed repositories have migrations at all — this
directory is part of the layout when there is a database, and should be deleted
when there is not.

**The tool is not chosen here.** `alembic` is the Python default;
`golang-migrate` and `atlas` are tool-agnostic and run the same way from CI or
from the application at start-up. Pick one, write it into `AGENTS.md`, and keep
the pairing rule whichever you pick: every migration that goes up must be able to
come back down.
