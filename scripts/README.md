# scripts

One-off operational scripts: a backfill, a data dump, a migration helper.

Nothing under `src/` imports anything here — that is the line between a script
and the product. If a script grows a second caller, it belongs in the package.
