Building a Simple Tokenizer for an English → Bengali Translation Task (From Scratch)

Goal: Learn how to build a simple tokenizer from scratch for an English → Bengali machine translation task without using libraries like Hugging Face or SentencePiece.

What You Will Learn

In this tutorial, we will build a complete tokenizer pipeline consisting of:

Define the dataset
Normalize text
Whitespace tokenization
Build the vocabulary
Add special tokens
Create token ↔ ID mappings
Encode sentences
Decode sentences
Pad sequences

By the end, you'll have tokenized and encoded data ready to feed into a simple Encoder–Decoder or Transformer model.

Project Structure
Raw Sentences
      │
      ▼
Normalize Text
      │
      ▼
Tokenize
      │
      ▼
Build Vocabulary
      │
      ▼
Assign IDs
      │
      ▼
Encode
      │
      ▼
Pad Sequences
      │
      ▼
Ready for Training
Step 1 — Define the Dataset

Let's start with a tiny English → Bengali translation dataset.

english_sentences = [
    "I like math .",
    "I like learning AI .",
    "I love deep learning ."
]

bengali_sentences = [
    "আমি গণিত পছন্দ করি ।",
    "আমি এআই শিখতে পছন্দ করি ।",
    "আমি ডিপ লার্নিং ভালোবাসি ।"
]

Our dataset consists of:

English	Bengali
I like math .	আমি গণিত পছন্দ করি ।
I like learning AI .	আমি এআই শিখতে পছন্দ করি ।
I love deep learning .	আমি ডিপ লার্নিং ভালোবাসি ।

Although tiny, this dataset is enough to understand every step of tokenization.

Step 2 — Normalize the Text

Before tokenization, we clean the text.

English
def normalize_english(sentence):
    return sentence.lower().strip()

Example:

"I Like Math ."
↓

"i like math ."

Lowercasing reduces the vocabulary size.

Without normalization:

Math
math
MATH

would become three different words.

Bengali
def normalize_bengali(sentence):
    return sentence.strip()

We only remove leading and trailing whitespace.

Unlike English, lowercasing isn't needed because Bengali has no uppercase/lowercase distinction.

After normalization:

English
i like math .
i like learning ai .
i love deep learning .
Bengali
আমি গণিত পছন্দ করি ।
আমি এআই শিখতে পছন্দ করি ।
আমি ডিপ লার্নিং ভালোবাসি ।
Step 3 — Tokenize the Sentences

A tokenizer converts a sentence into individual words (tokens).

We'll use the simplest tokenizer possible.

def tokenize(sentence):
    return sentence.split()
English Example

Input

i like math .

Output

["i", "like", "math", "."]
Bengali Example

Input

আমি গণিত পছন্দ করি ।

Output

["আমি", "গণিত", "পছন্দ", "করি", "।"]

The .split() function simply separates words using whitespace.

Step 4 — Build the Vocabulary

A neural network cannot understand words.

It only understands numbers.

Therefore, we need a vocabulary that maps every unique token to an integer.

First, define some special tokens.

SPECIAL_TOKENS = [
    "<PAD>",
    "<UNK>",
    "<SOS>",
    "<EOS>",
]
Why Do We Need Special Tokens?
Token	Meaning
<PAD>	Padding shorter sequences
<UNK>	Unknown word
<SOS>	Start of sentence
<EOS>	End of sentence

These tokens are essential for sequence models like Encoder–Decoder and Transformers.

Build the Vocabulary
def build_vocab(tokenized_sentences):

    vocab = set()

    for sentence in tokenized_sentences:
        vocab.update(sentence)

    vocab = SPECIAL_TOKENS + sorted(vocab)

    token_to_id = {
        token: idx
        for idx, token in enumerate(vocab)
    }

    id_to_token = {
        idx: token
        for token, idx in token_to_id.items()
    }

    return vocab, token_to_id, id_to_token
English Vocabulary
<PAD>
<UNK>
<SOS>
<EOS>
.
ai
deep
i
learning
like
love
math
Bengali Vocabulary
<PAD>
<UNK>
<SOS>
<EOS>
আমি
এআই
করি
গণিত
ডিপ
পছন্দ
ভালোবাসি
লার্নিং
শিখতে
।
Step 5 — Encode Tokens into IDs

Machine learning models operate on numbers rather than text.

The encoding process converts each token into its corresponding integer ID.

We also prepend the <SOS> token and append the <EOS> token to every sentence.

def encode(tokens, token_to_id):

    ids = []

    ids.append(token_to_id["<SOS>"])

    for token in tokens:
        ids.append(
            token_to_id.get(
                token,
                token_to_id["<UNK>"]
            )
        )

    ids.append(token_to_id["<EOS>"])

    return ids
Example

Sentence

i like math .

Tokenized

["i", "like", "math", "."]

Encoded

[2, 7, 9, 11, 4, 3]

Here:

2 → <SOS>

7 → i

9 → like

11 → math

4 → .

3 → <EOS>
Step 6 — Decode IDs Back into Tokens

Decoding performs the reverse operation.

def decode(ids, id_to_token):

    return [
        id_to_token[idx]
        for idx in ids
    ]

Example

Input

[2, 7, 9, 11, 4, 3]

Output

[
"<SOS>",
"i",
"like",
"math",
".",
"<EOS>"
]

This is useful for debugging and interpreting model outputs.

Step 7 — Pad the Sequences

Neural networks expect inputs in a batch to have the same length.

Consider these encoded sentences:

[2,7,9,11,4,3]

[2,7,9,8,5,4,3]

The second sentence is longer.

We pad the shorter sequence using the <PAD> token.

def pad_sequences(sequences, pad_id):

    max_length = max(
        len(sequence)
        for sequence in sequences
    )

    padded = []

    for sequence in sequences:

        new_sequence = sequence.copy()

        while len(new_sequence) < max_length:
            new_sequence.append(pad_id)

        padded.append(new_sequence)

    return padded

Example

Before

[2,7,9,11,4,3]

[2,7,9,8,5,4,3]

After

[2,7,9,11,4,3,0]

[2,7,9,8,5,4,3]

The shorter sentence receives one <PAD> token.

Step 8 — Vocabulary Mapping

The tokenizer maintains two dictionaries.

Token → ID
{
"<PAD>":0,
"<UNK>":1,
"<SOS>":2,
"<EOS>":3,
...
}
ID → Token
{
0:"<PAD>",
1:"<UNK>",
2:"<SOS>",
3:"<EOS>",
...
}

These mappings enable both encoding and decoding.

Step 9 — Final Training Data

After tokenization, encoding, and padding, our data is ready for training.

Example:

Encoder Input

[2,7,9,11,4,3,0]

Target Output

[2,4,7,9,6,13,3]

Each row now consists entirely of integers, making it suitable for neural networks.

Complete Pipeline Overview
English Sentence
       │
       ▼
Normalization
       │
       ▼
Whitespace Tokenizer
       │
       ▼
Tokens
       │
       ▼
Vocabulary
       │
       ▼
Token IDs
       │
       ▼
<SOS> + IDs + <EOS>
       │
       ▼
Padding
       │
       ▼
Tensor
       │
       ▼
Encoder
Time Complexity
Step	Complexity
Normalization	O(n)
Tokenization	O(n)
Vocabulary Building	O(n)
Encoding	O(n)
Decoding	O(n)
Padding	O(n)

Here, n represents the total number of tokens.

Limitations of This Tokenizer

While this tokenizer is useful for learning, it has several limitations:

It uses simple whitespace splitting.
It cannot split unknown words into smaller units.
It has no handling of punctuation beyond whitespace.
The vocabulary is fixed after construction.
It cannot effectively process rare or unseen words.

Modern NLP systems typically use subword tokenizers such as:

Byte Pair Encoding (BPE)
WordPiece
SentencePiece
Unigram Language Model

These approaches provide better handling of rare words, multilingual text, and open vocabularies.