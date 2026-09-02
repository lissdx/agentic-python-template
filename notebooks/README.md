# notebooks

Two genres with opposite policies. Mixing them is what turns this directory into
a junk drawer.

- **`experiments/`** — exploration. Runs against real inputs, so **strip the
  outputs before committing**: an output carries data into a history that does
  not forget. `nbstripout` installed once does this for you.
- **`tutorials/`** — for a reader. **Outputs are kept on purpose** — seeing what
  the code prints without running it is the point — and the data is synthetic.

Name files so they sort: `1.0-yl-retrieval-spike.ipynb`.

Nothing under `src/` imports a notebook. Code that earns a second caller moves
into the package.
