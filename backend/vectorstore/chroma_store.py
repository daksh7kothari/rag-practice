from functools import lru_cache
from pathlib import Path
import re


BASE_DIR = Path(__file__).resolve().parents[1]
TEXT_DIR = BASE_DIR / "data" / "text"

SOURCE_PRIORITY = {
    "faq.txt": 0,
    "docs.txt": 1,
    "doubts.txt": 2,
}

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


def _split_blocks(text: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            if current:
                blocks.append(current)
                current = []
            continue
        if line.startswith("#"):
            continue
        current.append(_normalize_line(line))

    if current:
        blocks.append(current)

    return blocks


def _parse_block(lines: list[str]) -> str | None:
    if not lines:
        return None

    has_question_answer = any(
        line.startswith("Q:") or line.startswith("A:") for line in lines
    )
    if has_question_answer:
        question_parts: list[str] = []
        answer_parts: list[str] = []
        plain_parts: list[str] = []
        mode: str | None = None

        for line in lines:
            if line.startswith("Q:"):
                mode = "q"
                question_parts.append(line[2:].strip())
            elif line.startswith("A:"):
                mode = "a"
                answer_parts.append(line[2:].strip())
            elif mode == "q":
                question_parts.append(line)
            elif mode == "a":
                answer_parts.append(line)
            else:
                plain_parts.append(line)

        question = " ".join(question_parts).strip()
        answer = " ".join(answer_parts).strip()
        plain = " ".join(plain_parts).strip()

        if question and answer:
            return f"Q: {question}\nA: {answer}"
        if question or answer:
            return " ".join(part for part in [question, answer, plain] if part).strip()

    return " ".join(lines).strip()


def _iter_text_files() -> list[Path]:
    if not TEXT_DIR.exists():
        return []

    def sort_key(path: Path) -> tuple[int, str]:
        return (SOURCE_PRIORITY.get(path.name, len(SOURCE_PRIORITY)), path.name)

    return sorted(TEXT_DIR.glob("*.txt"), key=sort_key)


def _load_records_from_file(path: Path) -> list[dict[str, str]]:
    content = path.read_text(encoding="utf-8", errors="ignore")

    if path.name == "doubts.txt":
        records: list[dict[str, str]] = []
        for raw_line in content.splitlines():
            line = _normalize_line(raw_line)
            if not line or line.startswith("#"):
                continue
            records.append({"source": path.name, "text": line})
        return records

    records: list[dict[str, str]] = []
    for block in _split_blocks(content):
        record = _parse_block(block)
        if not record:
            continue
        records.append({"source": path.name, "text": record})
    return records


@lru_cache(maxsize=1)
def _load_records() -> list[dict[str, str]]:
    records: list[dict[str, str]] = []

    for path in _iter_text_files():
        records.extend(_load_records_from_file(path))

    # Keep the source order but drop obvious duplicates.
    seen = set()
    deduped: list[dict[str, str]] = []
    for record in records:
        key = record["text"].lower()
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
        record_text = record["text"]
        record_tokens = _tokenize(record_text)
        if not record_tokens:
            continue

        overlap = len(query_tokens & record_tokens)
        if overlap == 0:
            continue

        source_bonus = 0.0
        if record["source"] == "faq.txt":
            source_bonus = 0.5
        elif record["source"] == "docs.txt":
            source_bonus = 0.25

        number_bonus = 0.25 if any(char.isdigit() for char in query) and any(
            char.isdigit() for char in record_text
        ) else 0.0
        length_bonus = min(len(record_text) / 2000.0, 0.25)
        score = overlap + source_bonus + number_bonus + length_bonus
        display_text = f"Source: {record['source']}\n{record_text}"
        scored.append((score, index, display_text))

    scored.sort(key=lambda item: (-item[0], item[1]))
    return [record for _, _, record in scored[:top_k]]


if __name__ == "__main__":
    print(f"Loaded {len(_load_records())} lightweight records from {TEXT_DIR}")
