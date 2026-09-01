# Architecture

_Replace this file with the shape of your system. What is here is scaffolding:
the questions worth answering before there is code to describe._

Only five of the thirteen surveyed repositories keep an architecture document at
all, and almost none of them call it `ARCHITECTURE.md` — the function is real,
the filename is not a convention. `browser-use` puts a README inside the package;
`prefect` keeps a section in `AGENTS.md`; `pydantic` uses
`docs/internals/architecture.md`. Put it where your readers already look.

## The shape

_The subsystems and what each one owns. If your `src/` tree is honest, this is
mostly a caption for it._

## The seams

_Where this system talks to something it does not control: the model provider,
the datastore, the outside API. Name the one file that owns each._

## The decisions and their costs

_What was chosen, what was rejected, and what the choice costs. This is the part
a reader cannot reconstruct from the code._

## What is not built yet

_Stated explicitly, so a reader stops looking for it._
