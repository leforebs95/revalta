from typing import BinaryIO, Dict, List
from PIL import Image
import fitz
import os
import uuid


class DocumentExtractor:
    """Handles splitting documents into pages"""

    def __init__(self, pages_dir: str):
        self.pages_dir = pages_dir
        os.makedirs(pages_dir, exist_ok=True)

    def extract_pages(self, document: BinaryIO) -> List[Dict]:
        """Extract pages from document into page directory

        Args:
            document: Binary document stream

        Returns:
            List of dicts containing:
                page_id: UUID of extracted page
                file_path: Path to extracted page file
                page_number: Page number in document
        """
        pass


class PDFExtractor(DocumentExtractor):
    """PDF specific document extraction"""

    def extract_pages(self, document: BinaryIO) -> List[Dict]:
        pages = []
        doc = fitz.open(stream=document.read(), filetype="pdf")

        for page_num in range(len(doc)):
            page = doc[page_num]
            pix = page.get_pixmap()

            page_id = uuid.uuid4()
            page_path = os.path.join(self.pages_dir, f"{page_id}.png")

            pix.save(page_path)

            pages.append(
                {"page_id": page_id, "file_path": page_path, "page_number": page_num}
            )

        return pages
