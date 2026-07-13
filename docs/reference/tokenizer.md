# Reference: `SimpleTokenizer`

**Module:** `src/rnn/tokenizer.py`

A from-scratch, whitespace tokenizer for an English → Bengali translation task.
No external tokenization libraries (Hugging Face, SentencePiece) are used. It maps
tokens to integer ids and back, and prepares padded id sequences ready to feed a
sequence model.

For the concepts and a guided walk-through, see the
[tutorial](../rnn/tokenizer.md). For rendering the animated explainer, see
[Render an animation](../how-to/render-animations.md).

```python
from src.rnn.tokenizer import SimpleTokenizer
```

## Class `SimpleTokenizer`

### `__init__(special_tokens: list[str] | None = None) -> None`

Creates a tokenizer with empty vocabulary maps.

| Parameter | Type | Default | Effect |
| --- | --- | --- | --- |
| `special_tokens` | `list[str] \| None` | `["<PAD>", "<UNK>", "<SOS>", "<EOS>"]` | Tokens placed at the front of the vocabulary, so their ids are stable. |

With the default special tokens the reserved ids are always:

| id | token | Meaning |
| --- | --- | --- |
| `0` | `<PAD>` | Padding for shorter sequences |
| `1` | `<UNK>` | Unknown / out-of-vocabulary token |
| `2` | `<SOS>` | Start of sequence |
| `3` | `<EOS>` | End of sequence |

**Attributes**

| Attribute | Type | Description |
| --- | --- | --- |
| `special_tokens` | `list[str]` | The reserved tokens. |
| `token_to_id` | `dict[str, int]` | Token → id map. Empty until `build_vocab` runs. |
| `id_to_token` | `dict[int, str]` | id → token map. Empty until `build_vocab` runs. |

### `normalize_english(sentence: str) -> str`

Lowercases and strips surrounding whitespace. Lowercasing collapses `Math`,
`MATH`, and `math` into a single token, keeping the vocabulary small.

```python
tok.normalize_english("  I Like Math .  ")  # -> "i like math ."
```

### `normalize_bengali(sentence: str) -> str`

Strips surrounding whitespace only. Bengali has no upper/lower case distinction,
so no case folding is applied.

```python
tok.normalize_bengali("  আমি গণিত পছন্দ করি ।  ")  # -> "আমি গণিত পছন্দ করি ।"
```

### `tokenize(sentence: str) -> list[str]`

Splits on whitespace via `str.split()`. Punctuation is only separated if it is
already surrounded by spaces (the sample data writes `.` and `।` as standalone
tokens).

```python
tok.tokenize("i like math .")  # -> ["i", "like", "math", "."]
```

### `build_vocab(tokenized_sentences: list[list[str]]) -> None`

Builds `token_to_id` and `id_to_token` from a corpus of tokenized sentences.
The vocabulary is `special_tokens` followed by the unique corpus tokens in
**sorted** order, so ids are deterministic for a given corpus.

```python
tok.build_vocab([["i", "like", "math", "."], ["i", "love", "ai", "."]])
# token_to_id == {"<PAD>":0,"<UNK>":1,"<SOS>":2,"<EOS>":3,
#                 ".":4,"ai":5,"i":6,"like":7,"love":8,"math":9}
```

> **Call `build_vocab` before `encode`, `decode`, or `pad_sequences`.** Those
> methods look up special-token ids; with an empty vocabulary they raise
> `KeyError`.

### `encode(tokens: list[str]) -> list[int]`

Maps tokens to ids, wrapping the result with `<SOS>` … `<EOS>`. Any token missing
from the vocabulary maps to `<UNK>` (id `1`).

```python
tok.encode(["i", "like", "math", "."])  # -> [2, 6, 7, 9, 4, 3]
```

| Behavior | Detail |
| --- | --- |
| Prefix | Always prepends `<SOS>`. |
| Suffix | Always appends `<EOS>`. |
| Unknown tokens | Fall back to `<UNK>` via `dict.get(token, unk_id)`. |

### `decode(ids: list[int]) -> list[str]`

Maps ids back to tokens. Useful for reading model output.

```python
tok.decode([2, 6, 7, 9, 4, 3])  # -> ["<SOS>", "i", "like", "math", ".", "<EOS>"]
```

> Unlike `encode`, `decode` does **not** have a fallback. An id that is not in
> `id_to_token` raises `KeyError`. Only pass ids produced against the same
> vocabulary.

### `pad_sequences(sequences: list[list[int]]) -> list[list[int]]`

Right-pads every sequence with the `<PAD>` id (`0`) to the length of the longest
sequence **in the batch passed in**. Non-mutating: returns new lists.

```python
tok.pad_sequences([[2, 6, 7, 3], [2, 6, 7, 9, 4, 3]])
# -> [[2, 6, 7, 3, 0, 0], [2, 6, 7, 9, 4, 3]]
```

## Module function

### `setup_utf8_output() -> None`

Rewraps `sys.stdout` / `sys.stderr` as UTF-8 if they are not already, so Bengali
text prints correctly on terminals that default to another encoding. Call it once
before printing tokenized Bengali.

## End-to-end example

```python
from src.rnn.tokenizer import SimpleTokenizer

sentences = ["i like math .", "i love deep learning ."]

tok = SimpleTokenizer()
tokenized = [tok.tokenize(s) for s in sentences]
tok.build_vocab(tokenized)

encoded = [tok.encode(t) for t in tokenized]
padded = tok.pad_sequences(encoded)
# padded is a rectangular list of ints, ready for a model
```

The [`run_tokenizer.py` demo](../how-to/development.md#run-the-tokenizer-demo)
runs this flow for both English and Bengali and logs the results.

## Related

- Tutorial: [Build a tokenizer from scratch](../rnn/tokenizer.md)
- How-to: [Render the tokenizer animation](../how-to/render-animations.md)
- Explanation: [Project architecture](../explanation/architecture.md)
