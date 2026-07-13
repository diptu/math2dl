# Math2DL Documentation

Math2DL explains deep learning through mathematics, Manim animations, and minimal
PyTorch implementations. This is the documentation hub.

The docs follow the [Diataxis](https://diataxis.fr/) framework — four kinds of
documentation, each written for a reader in a different mode:

| Quadrant | Reader is… | Start here |
| --- | --- | --- |
| **Tutorial** | learning by doing | [Build a tokenizer from scratch](rnn/tokenizer.md) |
| **How-to** | getting a task done | [Render an animation](how-to/render-animations.md) · [Set up for development](how-to/development.md) |
| **Reference** | looking up exact behavior | [`SimpleTokenizer` API](reference/tokenizer.md) |
| **Explanation** | understanding the design | [Project architecture](explanation/architecture.md) |

## What exists today

Math2DL is early-stage. Most architecture modules (`ann`, `cnn`, `gans`,
`transformers`) are placeholders on the [roadmap](../README.md#-learning-roadmap).
The first complete vertical slice is the **RNN tokenizer**, which shows the whole
Math2DL pipeline end to end:

```
docs/rnn/tokenizer.md          Tutorial  — the concepts, step by step
src/rnn/tokenizer.py           Code      — the SimpleTokenizer implementation
src/animations/rnn/tokenizer.py Animation — a Manim explainer of the pipeline
src/scripts/run_tokenizer.py   Demo      — runs the full pipeline on sample data
```

Use it as the template for how a topic is documented, coded, and animated.

## Quick links

- New here? Read the [tutorial](rnn/tokenizer.md), then run the demo:
  `uv run python -m src.scripts.run_tokenizer`
- Want to see the animation? Follow [Render an animation](how-to/render-animations.md).
- Setting up the repo? Follow [Set up for development](how-to/development.md).
- Curious why the code is laid out this way? Read the
  [architecture explanation](explanation/architecture.md).
