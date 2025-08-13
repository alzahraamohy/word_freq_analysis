import re
from collections import Counter
from typing import Iterable

# split on any non-word characters
_NON_WORD_RE = re.compile(r"\W+")

def tokens_from_chunks(chunks: Iterable[str]):
    carry = ""
    for chunk in chunks:
        text = (carry + chunk).lower()
        parts = _NON_WORD_RE.split(text)

        # If last character is alnum/underscore, last part might be an incomplete token
        if text and (text[-1].isalnum() or text[-1] == "_"):
            carry = parts[-1]
            parts = parts[:-1]
        else:
            carry = ""

        for p in parts:
            if p:
                yield p

    if carry:
        yield carry

def count_frequencies_from_chunks(chunks: Iterable[str]):
    """Count tokens from a streaming chunk source (memory-friendly)."""
    counter = Counter()
    for tok in tokens_from_chunks(chunks):
        counter[tok] += 1
    return counter
