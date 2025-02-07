import os
import fitz
from PIL import Image
import logging
import pytesseract
from typing import Dict, Optional, List
from datetime import datetime, timezone
import uuid
import requests

logger = logging.getLogger(__name__)


class PageProcessor:
    """Base class for handling different document types"""

    def get_page_count(self, file_path: str) -> int:
        raise NotImplementedError

    def extract_page(self, file_path: str, page_number: int) -> str:
        raise NotImplementedError


class PDFProcessor(PageProcessor):
    def __init__(self, page_dir: str):
        self.page_dir = page_dir
        os.makedirs(page_dir, exist_ok=True)
        self.file_service_url = "http://file-api:5001"

    def _download_file(self, file_id, filename):
        """Download file from file service."""
        try:
            response = requests.get(
                f"{self.file_service_url}/api/files/{file_id}/download", stream=True
            )
            if response.status_code == 200:
                temp_path = os.path.join(self.page_dir, filename)
                with open(temp_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return temp_path
        except Exception as e:
            logger.error(f"Failed to download file {file_id}: {str(e)}")
            return None

    def get_page_count(self, file_path: str) -> int:
        doc = fitz.open(file_path)
        return len(doc)

    def extract_page(self, file_path: str, page_number: int) -> str:
        doc = fitz.open(file_path)
        page = doc[page_number]
        pix = page.get_pixmap()

        # Generate unique filename for this page
        page_id = uuid.uuid4()
        page_filename = os.path.join(self.page_dir, f"{page_id}.png")

        # Save page as PNG
        pix.save(page_filename)

        return page_id, page_filename


class OCRProcessor:
    """Handles OCR processing using Tesseract."""

    def __init__(self, page_dir="/usr/src/ocr-service/pages"):
        self.page_dir = page_dir
        self.processors = {"pdf": PDFProcessor(page_dir)}

    def process_page(self, page_path: str) -> Optional[Dict]:
        """Process a single page through OCR."""
        try:
            # Load page image
            image = Image.open(page_path)

            # Extract text using tesseract
            text = pytesseract.image_to_string(image)

            # Get additional data like confidence scores
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            # Calculate average confidence excluding -1 values
            confidence_scores = [score for score in data["conf"] if score != -1]
            avg_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 0
            )

            return {
                "text": text,
                "raw_data": data,
                "confidence": avg_confidence,
                "status": "complete",
                "page_path": page_path,
            }

        except Exception as e:
            logger.error(f"Failed to process page {page_path}: {str(e)}")
            return {
                "text": None,
                "raw_data": None,
                "confidence": 0,
                "status": "failed",
                "error_message": str(e),
                "page_path": page_path,
            }

    def retry_page(self, doc_page) -> bool:
        """Retry processing a failed page."""
        try:
            result = self.process_page(doc_page.page_path)

            doc_page.text_content = result["text"]
            doc_page.raw_data = result["raw_data"]
            doc_page.confidence = result["confidence"]
            doc_page.status = result["status"]
            doc_page.error_message = result.get("error_message")
            doc_page.retry_count += 1
            doc_page.last_attempt = datetime.now(timezone.utc)

            return doc_page.status == "complete"

        except Exception as e:
            logger.error(f"Retry failed for page {doc_page.page_path}: {str(e)}")
            return False

    def _get_file_type(self, file_path: str) -> str:
        """Determine file type from extension."""
        return file_path.split(".")[-1].lower()

    def process_file(self, file_id: str, filename: str) -> Dict:
        """Process all pages in a document."""

        file_path = self._download_file(file_id, filename)
        try:
            file_type = self._get_file_type(file_path)
            processor = self.processors.get(file_type)

            if not processor:
                raise ValueError(f"Unsupported file type: {file_type}")

            page_count = processor.get_page_count(file_path)
            successes = 0
            failures = 0
            results = []

            # Extract and process each page
            for page_num in range(page_count):
                page_path = processor.extract_page(file_path, page_num)
                result = self.process_page(page_path)
                result["page_number"] = page_num

                if result["status"] == "complete":
                    successes += 1
                else:
                    failures += 1
                results.append(result)

            return {
                "total_pages": page_count,
                "successful_pages": successes,
                "failed_pages": failures,
                "page_results": results,
            }

        except Exception as e:
            logger.error(f"Failed to process file {file_path}: {str(e)}")
            return None
