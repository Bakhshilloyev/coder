"""Small text utilities used by prompts and tools."""

from typing import List


def truncate(text: str, max_len: int = 4000, suffix: str = "…") -> str:
    if len(text) <= max_len:
        return text
    return text[: max_len - len(suffix)] + suffix


def chunk_text(text: str, size: int = 4000, overlap: int = 0) -> List[str]:
    """Split *text* into chunks of at most *size* characters.

    Useful on weak devices to avoid loading huge blobs into memory.
    """
    if size <= 0:
        raise ValueError("size must be positive")
    if not text:
        return [""]
    step = max(1, size - overlap)
    return [text[i : i + size] for i in range(0, len(text), step)]


def strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text


def count_tokens_approx(text: str) -> int:
    """Rough token estimate (~4 chars/token) for budget checks."""
    return max(1, len(text) // 4)
