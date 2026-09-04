# data/

Local working data: the corpus you index, downloaded datasets, scratch inputs.
Delete this directory if your project has no local data at all.

By default nothing here is committed — `.gitignore` carries `data/*` with this
file as the only exception. The reasons: real inputs are large, change
independently of the code, and often carry private or third-party content —
and git history does not forget.

This is a default, not a prohibition. Committing a small, open, synthetic
sample is a legitimate, deliberate act: `git add -f data/<file>` or narrow the
`.gitignore` rule. The decision stays with you; the default only guards the
irreversible mistake.

The canonical corpus lives outside the repository (object storage, a shared
bucket). The code that fetches and indexes it lives in the package —
`retrieval/`.
