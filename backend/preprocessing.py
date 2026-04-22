import re
from typing import List

from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

STOP_WORDS = set(ENGLISH_STOP_WORDS)


def preprocess_text(text: str, use_lemmatization: bool = False) -> str:
    """
    Clean text using:
    1) lowercasing
    2) tokenization
    3) stopword removal
    4) optional lemmatization
    """
    if not isinstance(text, str):
        raise ValueError("Input text must be a string.")

    lower_text = text.lower()
    alphanumeric_only = re.sub(r"[^a-z0-9\s]", " ", lower_text)
    # Regex tokenization keeps this function independent of external downloads.
    tokens: List[str] = re.findall(r"\b[a-z0-9]+\b", alphanumeric_only)

    filtered_tokens = [
        token for token in tokens if token not in STOP_WORDS and len(token.strip()) > 1
    ]

    # Optional lightweight normalization (basic suffix trimming).
    if use_lemmatization:
        normalized_tokens: List[str] = []
        for token in filtered_tokens:
            if token.endswith("ies") and len(token) > 4:
                normalized_tokens.append(token[:-3] + "y")
            elif token.endswith("s") and len(token) > 3:
                normalized_tokens.append(token[:-1])
            else:
                normalized_tokens.append(token)
        filtered_tokens = normalized_tokens

    return " ".join(filtered_tokens)
