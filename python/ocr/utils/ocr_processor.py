from abc import ABC, abstractmethod
import os
from typing import Dict

import boto3
import pytesseract
from PIL import Image
from dotenv import load_dotenv

from utils.llm_clients.anthropic import AnthropicClient
import logging

load_dotenv()
# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseOCRProcessor(ABC):
    """Base class for OCR processing"""

    @abstractmethod
    def process_page(self, page_path: str) -> Dict:
        """Process a single page and extract text

        Args:
            page_path: Path to page image file

        Returns:
            Dict containing OCR results:
                text: Extracted text content
                raw_data: Raw OCR data
                confidence: Confidence score
                status: Processing status
                error_message: Optional error message if failed
        """
        pass

    def _format_response(
        self,
        text: str,
        raw_data: Dict,
        confidence: float,
        status: str,
        error_message: str = None,
    ) -> Dict:
        """Format standard OCR response

        Args:
            text: Extracted text content
            raw_data: Raw OCR output data
            confidence: Confidence score
            status: Processing status
            error_message: Optional error message

        Returns:
            Dict with standard OCR response format
        """
        return {
            "text": text,
            "raw_data": raw_data,
            "confidence": confidence,
            "status": status,
            "error_message": error_message,
        }

    def _handle_error(self, error: Exception) -> Dict:
        """Handle OCR processing error

        Args:
            error: Exception that occurred

        Returns:
            Dict with error response format
        """
        return self._format_response(
            text=None,
            raw_data=None,
            confidence=0,
            status="failed",
            error_message=str(error),
        )


class TesseractProcessor(BaseOCRProcessor):
    """OCR processor using Tesseract"""

    def process_page(self, page_path: str) -> Dict:
        try:
            image = Image.open(page_path)
            text = pytesseract.image_to_string(image)
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

            confidence_scores = [score for score in data["conf"] if score != -1]
            avg_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 0
            )

            return self._format_response(
                text=text, raw_data=data, confidence=avg_confidence, status="complete"
            )

        except Exception as e:
            return self._handle_error(e)


class AWSTextractProcessor(BaseOCRProcessor):
    """OCR processor using AWS Textract"""

    def __init__(self, region: str = "us-west-2"):
        self.client = boto3.client("textract", region_name=region)

    def process_page(self, page_path: str) -> Dict:
        # Implementation to process page using AWS Textract
        try:
            with open(page_path, "rb") as file:
                response = self.client.detect_document_text(
                    Document={"Bytes": file.read()}
                )

            # Extract text blocks
            text_blocks = []
            for block in response["Blocks"]:
                if block["BlockType"] == "LINE":
                    text_blocks.append(
                        {
                            "text": block["Text"],
                            "confidence": block["Confidence"],
                            "boundingBox": block["Geometry"]["BoundingBox"],
                        }
                    )
                # For now just take lines
                # elif block["BlockType"] == "WORD":
                #     text_blocks.append(
                #         {
                #             "text": block["Text"],
                #             "confidence": block["Confidence"],
                #             "boundingBox": block["Geometry"]["BoundingBox"],
                #             "type": "word",
                #         }
                #     )

            confidence_scores = [block["confidence"] for block in text_blocks]
            avg_confidence = (
                sum(confidence_scores) / len(confidence_scores)
                if confidence_scores
                else 0
            )

            text = "\n".join([block["text"] for block in text_blocks])
            improver = AnthropicClient(api_key=os.environ.get("ANTHROPIC_API_KEY"))
            logger.info(f"Original text: {text}")
            improved_text = improver.generate(prompt=text)
            logger.info(f"Improved text: {improved_text}")

            return self._format_response(
                text=improved_text,
                raw_data=response,
                confidence=avg_confidence,
                status="complete",
            )
        except Exception as e:
            return self._handle_error(e)
