# How to set up for development

Get a working environment, run the quality gates, and run the tokenizer demo.

## Prerequisites

- **Python 3.12** (pinned in `.python-version`).
- **[uv](https://docs.astral.sh/uv/)** for environment and dependency management.
- **make** (optional but convenient — every workflow below has a `make` target).

## Install the environment

```bash
make init     # create the .venv (Python 3.12) and sync all dependencies
# or, without make:
uv venv --python 3.12
uv sync
```

`make init` also creates the source and asset directories if they are missing.
To only re-sync dependencies after a `pyproject.toml` change:

```bash
make sync     # == uv sync
```

## Run the quality gates

The project enforces lint, type-check, and tests. Run them all with:

```bash
make check    # lint + typecheck + test
```

Individual gates:

| Command | Tool | What it does |
| --- | --- | --- |
| `make lint` | Ruff | Lints `.` (no changes). Rule set: `E, F, I, UP, ANN, B, PL`. |
| `make format` | Ruff | Auto-formats and applies safe lint fixes. |
| `make typecheck` | mypy | Strict type-checks `src`. |
| `make test` | pytest | Runs the suite in `src/tests`. |

Configuration for all of these lives in `pyproject.toml` (`[tool.ruff]`,
`[tool.mypy]`, `[tool.pytest.ini_options]`).

> **Note:** `src/tests` currently has no test files, so `make test` (and therefore
> `make check`) exits non-zero with pytest's "no tests ran" code (5). Adding the
> first test under `src/tests/` clears this.

## Run the tokenizer demo

The demo runs the full English → Bengali pipeline and logs each padded sample.
Run it as a **module** from the repo root (running the file directly fails,
because it imports the top-level `src` package):

```bash
uv run python -m src.scripts.run_tokenizer
```

Expected output (one structured log line per sample):

```
... | INFO | Inference sample processed | {'sample_index': 0,
       'encoder_input': [2, 7, 9, 11, 4, 3, 0],
       'target_output':  [2, 5, 8, 10, 7, 4, 3, 0], ...}
```

Set `LOG_MODE=prod` for JSON logs instead of the colored dev format:

```bash
LOG_MODE=prod uv run python -m src.scripts.run_tokenizer
```

## Render an animation

See [Render an animation](render-animations.md).

## Clean up

```bash
make clean    # remove .venv, media/, and caches
```

## Related

- Explanation: [Project architecture](../explanation/architecture.md)
- Reference: [`SimpleTokenizer` API](../reference/tokenizer.md)
