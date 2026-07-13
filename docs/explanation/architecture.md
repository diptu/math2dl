# Explanation: Project architecture

This explains how Math2DL is organized and why. It is background, not a
step-by-step guide — for those, see the [how-to guides](../README.md).

## The problem

Math2DL teaches deep learning by pairing three things for every topic: the
**mathematics**, an **animation** that builds intuition, and a **minimal
implementation** you can read in one sitting. That is three artifacts per topic,
across a dozen planned topics (ANN, CNN, RNN, Transformers, GANs, …).

Without structure this sprawls fast: animation code tangled with model code,
docs drifting from the implementation they describe, and no obvious place for a
new topic to go. The layout below keeps each topic self-similar so a contributor
who has seen one topic can navigate any other.

## The pedagogical pipeline

Every topic is meant to move the reader along the same path:

```
Mathematics → Geometric intuition → Animation → Implementation → Real DL model
```

The repository mirrors that pipeline in where files live: the math and intuition
go in `docs/`, the animation in `src/animations/`, and the implementation in the
topic package (`src/rnn/`, `src/cnn/`, …).

## Directory layout

```
math2dl/
├── docs/                  # prose: tutorials, how-tos, reference, explanation
│   └── rnn/tokenizer.md   #   the RNN tokenizer tutorial
├── src/
│   ├── animations/        # Manim scenes, mirrored by topic
│   │   └── rnn/tokenizer.py
│   ├── ann/  cnn/  rnn/    # topic packages: the minimal implementations
│   ├── gans/ transformers/
│   ├── common/            # shared helpers across topics
│   ├── core/              # cross-cutting config/logging (currently stubs)
│   └── scripts/           # runnable demos and entry points
├── Makefile               # init / sync / render / lint / typecheck / test
├── pyproject.toml         # deps, tool config, wheel packaging
└── uv.lock                # pinned dependency graph
```

### Flat, topic-per-package layout

`pyproject.toml` packages each topic as a **top-level importable package**:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/ann", "src/cnn", "src/rnn", "src/gans",
            "src/transformers", "src/common"]
```

So the built wheel exposes `import rnn`, `import cnn`, and so on — flat, not
`math2dl.rnn`. Each topic is an independent unit that can be understood and
imported on its own.

Note what is **not** shipped in the wheel: `animations/`, `core/`, and `scripts/`.
Those are development-side. Animations are large and Manim-specific; scripts are
demos, not library API. The distributed package is just the minimal
implementations a learner would import.

> **Two import styles coexist today.** Demos under `src/scripts/` import the
> source tree with the `src.` prefix (`from src.rnn.tokenizer import ...`), which
> is why they run as modules from the repo root
> (`python -m src.scripts.run_tokenizer`). The wheel, by contrast, flattens
> `src/` away so installed code imports `rnn.tokenizer`. Keep this in mind when
> moving code between a demo and the shipped package.

### Mirroring: implementation ↔ animation ↔ docs

A topic appears in three places under the same name:

| Concern | Path | Example |
| --- | --- | --- |
| Implementation | `src/<topic>/` | `src/rnn/tokenizer.py` |
| Animation | `src/animations/<topic>/` | `src/animations/rnn/tokenizer.py` |
| Prose | `docs/<topic>/` | `docs/rnn/tokenizer.md` |

The tokenizer is the first complete example of all three. New topics should
follow the same three-way mirror.

## Tooling choices

| Choice | Why |
| --- | --- |
| **uv** | Fast, reproducible installs; `uv.lock` is committed for a pinned graph. |
| **Ruff** (`E, F, I, UP, ANN, B, PL`) | One fast tool for lint + import sorting + formatting. `ANN` enforces type annotations, which matters for ML code where shapes and dtypes are easy to get wrong. |
| **mypy strict** | Catches type errors early; the NumPy mypy plugin adds dtype/shape precision. |
| **Manim Community 0.20** | Renders through PyAV (no separate `ffmpeg` CLI needed). |
| **loguru** | Structured logging with a colored dev format and a JSON `prod` mode (`LOG_MODE`). |

## Trade-offs

- **Flat packages** keep each topic independent and importable, at the cost of a
  slightly unusual `src.`-prefixed import path for in-repo demos. The two import
  styles above are the price of that choice.
- **Mirroring across three trees** means a topic is split across `docs/`,
  `src/<topic>/`, and `src/animations/<topic>/` rather than colocated. The payoff
  is clean packaging (only implementations ship) and predictable navigation.
- **Early-stage stubs.** `main.py`, `Dockerfile`, `src/core/config.py`, and most
  topic packages are placeholders. The repository is scaffolding plus one complete
  vertical slice (the tokenizer). Treat the [roadmap](../../README.md#-learning-roadmap)
  as the source of truth for what is real versus planned.

## Related

- Reference: [`SimpleTokenizer` API](../reference/tokenizer.md)
- How-to: [Set up for development](../how-to/development.md) ·
  [Render an animation](../how-to/render-animations.md)
- Tutorial: [Build a tokenizer from scratch](../rnn/tokenizer.md)
