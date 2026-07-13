# How to render an animation

Render a Manim scene to a video (or a single frame) and preview it.

## Prerequisites

- The project environment is installed (`make sync` or `uv sync`). See
  [Set up for development](development.md).
- Manim's system dependencies are available. Manim Community 0.20 renders through
  [PyAV](https://pyav.org/), which ships as a wheel, so no separate `ffmpeg`
  binary is required for MP4 output.
- Bengali scenes use the system font **Baloo Da 2** (bundled with macOS). On other
  platforms, install a Bengali font or the Bengali text renders as empty boxes.

## Available scenes

| Scene | File | What it shows |
| --- | --- | --- |
| `TokenizerPipeline` | `src/animations/rnn/tokenizer.py` | The full tokenizer pipeline: dataset → normalize → tokenize → vocabulary → encode → decode → pad → ready for training. |

## Steps

1. Render with the Makefile target. `SCENE` is `path/to/file.py:ClassName`:

   ```bash
   make render SCENE=src/animations/rnn/tokenizer.py:TokenizerPipeline
   ```

   This runs `manim -pqh` — **p**review (opens the player when done) at **h**igh
   quality. The finished file lands at:

   ```
   media/videos/tokenizer/1080p60/TokenizerPipeline.mp4
   ```

2. Or call Manim directly for more control over quality and flags:

   ```bash
   # High quality, opens a preview when done
   uv run manim -pqh src/animations/rnn/tokenizer.py TokenizerPipeline

   # Low quality, fast — use while iterating
   uv run manim -pql src/animations/rnn/tokenizer.py TokenizerPipeline
   ```

   Common quality flags: `-ql` (480p15), `-qm` (720p30), `-qh` (1080p60),
   `-qk` (4K). Add `--disable_caching` if you changed code but Manim reuses a
   cached partial movie.

## Verification

The command prints the output path and ends with a line like:

```
INFO   Rendered TokenizerPipeline
       Played 68 animations
```

The MP4 exists under `media/videos/…`. With `-p`, the system video player opens
automatically.

To grab a single still without a video player (Manim 0.20 uses PyAV, not the
`ffmpeg` CLI):

```python
import av
container = av.open("media/videos/tokenizer/480p15/TokenizerPipeline.mp4")
stream = container.streams.video[0]
for frame in container.decode(video=0):
    if float(frame.pts * stream.time_base) >= 30:  # seconds
        frame.to_image().save("frame.png")
        break
```

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `TypeError: can only concatenate str (not "NoneType") to str` | A `Text(..., font=None)` was passed explicitly. | Omit the `font` argument instead of passing `None`. |
| Bengali text renders as empty boxes (tofu) | No Bengali font on the system. | Install a Bengali font (e.g. Noto Sans Bengali) and set it via the `font=` argument on `Text`. |
| Code changes don't appear in the video | Manim reused a cached partial movie. | Re-render with `--disable_caching`. |
| `make render` prints the usage line and does nothing | `SCENE` was not provided. | Pass `SCENE=path/to/file.py:ClassName`. |

## Clean up render artifacts

Rendered videos live under `media/` (git-ignored). Remove them with:

```bash
make clean   # also removes .venv and caches
```

## Related

- Reference: [`SimpleTokenizer` API](../reference/tokenizer.md)
- Tutorial: [Build a tokenizer from scratch](../rnn/tokenizer.md)
