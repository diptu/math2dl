"""
Simple Tokenizer for an English → Bengali Translation Task
dataset : https://www.kaggle.com/datasets/sayedshaun/english-to-bengali-for-machine-translation
"""

import io
import sys


def setup_utf8_output() -> None:
    if sys.stdout.encoding != "UTF-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")


class SimpleTokenizer:
    def __init__(self, special_tokens: list[str] | None = None) -> None:
        self.special_tokens = special_tokens or ["<PAD>", "<UNK>", "<SOS>", "<EOS>"]
        self.token_to_id: dict[str, int] = {}
        self.id_to_token: dict[int, str] = {}

    def normalize_english(self, sentence: str) -> str:
        return sentence.lower().strip()

    def normalize_bengali(self, sentence: str) -> str:
        return sentence.strip()

    def tokenize(self, sentence: str) -> list[str]:
        return sentence.split()

    def build_vocab(self, tokenized_sentences: list[list[str]]) -> None:
        vocab = set(token for sent in tokenized_sentences for token in sent)
        sorted_vocab = self.special_tokens + sorted(list(vocab))
        self.token_to_id = {token: idx for idx, token in enumerate(sorted_vocab)}
        self.id_to_token = {idx: token for token, idx in self.token_to_id.items()}

    def encode(self, tokens: list[str]) -> list[int]:
        ids = [self.token_to_id["<SOS>"]]
        ids.extend(
            [self.token_to_id.get(token, self.token_to_id["<UNK>"]) for token in tokens]
        )
        ids.append(self.token_to_id["<EOS>"])
        return ids

    def decode(self, ids: list[int]) -> list[str]:
        return [self.id_to_token[idx] for idx in ids]

    def pad_sequences(self, sequences: list[list[int]]) -> list[list[int]]:
        max_length = max(len(seq) for seq in sequences)
        pad_id = self.token_to_id["<PAD>"]
        return [seq + [pad_id] * (max_length - len(seq)) for seq in sequences]
