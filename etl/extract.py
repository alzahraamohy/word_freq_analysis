import chardet
from typing import Generator

#Detect text encoding (reads first 100KB)
def detect_encoding(file_path: str) -> str:
    with open(file_path, "rb") as f:
        raw = f.read(100_000)
    result = chardet.detect(raw)
    return result.get("encoding") or "utf-8"

#Read file in chunks to avoid memory issues with large files (IMB size)
def read_file_in_chunks(file_path: str, chunk_size: int = 1024 * 1024) -> Generator[str, None, None]:
    enc = detect_encoding(file_path)
    with open(file_path, "r", encoding=enc, errors="ignore") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk
