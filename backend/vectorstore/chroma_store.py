from functools import lru_cache
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parents[1]
CORPUS_PATH = BASE_DIR / "data" / "text" / "doubts.txt"

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "at",
    "can",
    "for",
    "from",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "to",
    "was",
    "what",
    "when",
    "where",
    "which",
    "who",
    "will",
    "with",
    "you",
    "your",
    "tomorrow",
    "today",
    "day",
}


def _tokenize(text: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOPWORDS
    }


def _normalize_line(line: str) -> str:
    return re.sub(r"\s+", " ", line.strip())


@lru_cache(maxsize=1)
def _load_records() -> list[str]:
    if not CORPUS_PATH.exists():
        return []

    records: list[str] = []
    previous_line = ""

    for raw_line in CORPUS_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = _normalize_line(raw_line)
        if not line:
            previous_line = ""
            continue

        if line.startswith(">"):
            answer = line.lstrip(">").strip()
            if previous_line:
                records.append(f"{previous_line}\n{answer}")
            else:
                records.append(answer)
            previous_line = ""
            continue

        if previous_line:
            records.append(previous_line)

        previous_line = line

    if previous_line:
        records.append(previous_line)

    # Keep the source order but drop obvious duplicates.
    seen = set()
    deduped: list[str] = []
    for record in records:
        key = record.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(record)

    return deduped


def store_chunks(chunks: list[str], embeddings=None) -> bool:
    """
    Compatibility shim for the older ingestion flow.

    The Render-friendly version keeps the source corpus in text form instead of
    persisting embeddings to a local vector database.
    """

    return bool(chunks)


def search(query: str, top_k: int = 5) -> list[str]:
    """
    Search the local text corpus using lightweight keyword overlap.
    """

    query_tokens = _tokenize(query)
    records = _load_records()
    if not records:
        return []

    scored: list[tuple[float, int, str]] = []
    for index, record in enumerate(records):
        record_tokens = _tokenize(record)
        if not record_tokens:
            continue

        overlap = len(query_tokens & record_tokens)
        if overlap == 0:
            continue

        number_bonus = 0.25 if any(char.isdigit() for char in query) and any(
            char.isdigit() for char in record
        ) else 0.0
        length_bonus = min(len(record) / 2000.0, 0.25)
        score = overlap + number_bonus + length_bonus
        scored.append((score, index, record))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [record for _, _, record in scored[:top_k]]


if __name__ == "__main__":
    print(f"Loaded {len(_load_records())} lightweight records from {CORPUS_PATH}")
