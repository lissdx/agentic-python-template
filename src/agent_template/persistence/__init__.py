"""Optional. Delete this package if nothing outlives the process.

Durable state: checkpoints, run history, repositories over whatever store is in
use. This is the only place that knows the storage engine — the rest of the
package asks for a repository and never for a connection.

Migrations do not live here. They live in `db/migrations/` outside the package,
because a migration tool executes them and Python never imports them.
"""
