import os
import sys

from loguru import logger

from src.rnn.tokenizer import SimpleTokenizer, setup_utf8_output

# Configuration: Check environment
LOG_MODE = os.getenv("LOG_MODE", "dev")


def setup_logging() -> None:
    # Remove any existing handlers
    logger.remove()

    if LOG_MODE == "dev":
        # Human-readable output for the terminal
        logger.add(
            sys.stderr,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level>"
                "| <cyan>{message}</cyan> | <magenta>{extra}</magenta>"
            ),
            level="INFO",
            colorize=True,
            serialize=False,  # Crucial: Must be False for colors/formatting
        )
    else:
        # Structured JSON for production (e.g., streaming to a file or collector)
        logger.add(
            sys.stderr,
            serialize=True,  # This forces the JSON format
            level="INFO",
        )


def main() -> None:
    setup_logging()
    setup_utf8_output()

    # ... [Rest of your initialization code remains the same] ...
    en_tok = SimpleTokenizer()
    bn_tok = SimpleTokenizer()
    raw_english = ["I like math .", "I like learning AI .", "I love deep learning ."]
    raw_bengali = [
        "আমি গণিত পছন্দ করি ।",
        "আমি এআই শিখতে পছন্দ করি ।",
        "আমি ডিপ লার্নিং ভালোবাসি ।",
    ]

    en_clean = [en_tok.normalize_english(s) for s in raw_english]
    bn_clean = [bn_tok.normalize_bengali(s) for s in raw_bengali]
    en_tokens = [en_tok.tokenize(s) for s in en_clean]
    bn_tokens = [bn_tok.tokenize(s) for s in bn_clean]
    en_tok.build_vocab(en_tokens)
    bn_tok.build_vocab(bn_tokens)
    en_encoded = [en_tok.encode(s) for s in en_tokens]
    bn_encoded = [bn_tok.encode(s) for s in bn_tokens]
    en_padded = en_tok.pad_sequences(en_encoded)
    bn_padded = bn_tok.pad_sequences(bn_encoded)

    # Structured Output
    for i, (src, tgt) in enumerate(zip(en_padded, bn_padded, strict=False)):
        src_data = src.tolist() if hasattr(src, "tolist") else src
        tgt_data = tgt.tolist() if hasattr(tgt, "tolist") else tgt

        logger.info(
            "Inference sample processed",
            sample_index=i,
            encoder_input=src_data,
            target_output=tgt_data,
            input_length=len(src_data),
            target_length=len(tgt_data),
        )


if __name__ == "__main__":
    main()
