from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TextChunk:
    text: str
    seq_number: int
    metadata: Dict


class DocumentChunker:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_document(self, text: str) -> List[TextChunk]:
        """Split document into overlapping chunks"""
        chunks = []
        start = 0
        chunk_num = 0

        while start < len(text):
            # Get chunk with overlap
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end]

            # Create chunk with metadata
            chunk = TextChunk(
                text=chunk_text,
                seq_number=chunk_num,
                metadata={
                    "start_char": start,
                    "end_char": end,
                },
            )
            chunks.append(chunk)

            # Move start position accounting for overlap
            start = end - self.chunk_overlap
            chunk_num += 1

        return chunks
