-- Runs once, when the data directory is created. Postgres ignores this file on
-- every later start, so it holds only what must exist before anything else:
-- extensions, roles, schemas. Table definitions belong in db/migrations/, where
-- a migration tool can version them and roll them back.

CREATE EXTENSION IF NOT EXISTS vector;
