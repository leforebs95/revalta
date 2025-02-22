from concurrent.futures import ThreadPoolExecutor
from http import HTTPStatus
import os
from flask import jsonify, current_app, send_file
from app.models import db, DocumentPage
from utils.ocr_processor import TesseractProcessor, AWSTextractProcessor
from utils.file_provider import UploadServiceProvider
from utils.document_extractor import PDFExtractor

from . import ocr


@ocr.route("/api/ocr/version")
def version():
    return jsonify({"version": "1.0.0"})


@ocr.route("/api/ocr/document/<uuid:file_id>/extract", methods=["POST"])
def extract_document(file_id):
    """Extract pages from document and create records"""
    try:
        # Get document from upload service
        provider = UploadServiceProvider("http://uploads-api:5001/api/uploads")
        document = provider.get_file(file_id)

        # Extract pages from document
        extractor = PDFExtractor(current_app.config["PAGES_LOCATION"])
        pages = extractor.extract_pages(document)

        # Create document pages records
        for page in pages:
            doc_page = DocumentPage(
                page_id=page["page_id"],
                file_id=file_id,
                page_number=page["page_number"],
                page_path=page["file_path"],
                status="pending",
            )
            db.session.add(doc_page)

        db.session.commit()

        return (
            jsonify(
                {
                    "file_id": file_id,
                    "page_count": len(pages),
                    "pages": [
                        {"page_id": p["page_id"], "page_number": p["page_number"]}
                        for p in pages
                    ],
                }
            ),
            HTTPStatus.CREATED,
        )

    except Exception as e:
        current_app.logger.error(f"Error extracting document: {str(e)}")
        return (
            jsonify({"error": "Failed to extract document pages"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@ocr.route("/api/ocr/document/<uuid:file_id>/process", methods=["POST"])
def process_document(file_id):
    """Process extracted pages with OCR"""
    try:
        pages = (
            DocumentPage.query.filter_by(file_id=file_id, status="pending")
            .order_by(DocumentPage.page_number)
            .all()
        )

        if not pages:
            return (
                jsonify({"error": "No pending pages found for document"}),
                HTTPStatus.NOT_FOUND,
            )

        # processor = TesseractProcessor()
        processor = AWSTextractProcessor()
        processed = []

        for page in pages:
            result = processor.process_page(page.page_path)

            page.text_content = result["text"]
            page.raw_data = result["raw_data"]
            page.confidence = result["confidence"]
            page.status = result["status"]
            page.error_message = result.get("error_message")

            db.session.commit()

            processed.append(
                {
                    "page_id": page.page_id,
                    "page_number": page.page_number,
                    "status": page.status,
                }
            )

        return jsonify({"file_id": file_id, "processed_pages": processed})

    except Exception as e:
        current_app.logger.error(f"Error processing document: {str(e)}")
        return (
            jsonify({"error": "Failed to process document"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@ocr.route("/api/ocr/document/<uuid:file_id>")
def get_document(file_id):
    """Get OCR results for a document"""
    try:
        pages = (
            DocumentPage.query.filter_by(file_id=file_id)
            .order_by(DocumentPage.page_number)
            .all()
        )

        if not pages:
            return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND

        return jsonify([page.to_dict() for page in pages])

    except Exception as e:
        current_app.logger.error(f"Error getting document: {str(e)}")
        return (
            jsonify({"error": "Failed to get document"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@ocr.route("/api/ocr/document/<uuid:file_id>/status")
def get_status(file_id):
    """Get document processing status"""
    try:
        pages = DocumentPage.query.filter_by(file_id=file_id).all()

        if not pages:
            return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND

        status = {
            "total": len(pages),
            "complete": sum(1 for p in pages if p.status == "complete"),
            "pending": sum(1 for p in pages if p.status == "pending"),
            "failed": sum(1 for p in pages if p.status == "failed"),
        }

        return jsonify(status)

    except Exception as e:
        current_app.logger.error(f"Error getting status: {str(e)}")
        return (
            jsonify({"error": "Failed to get status"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@ocr.route("/api/ocr/page/<uuid:page_id>")
def get_page(page_id):
    """Get OCR result for specific page"""
    try:
        page = DocumentPage.query.filter_by(page_id=page_id).first()

        if not page:
            return jsonify({"error": "Page not found"}), HTTPStatus.NOT_FOUND

        return jsonify(page.to_dict())

    except Exception as e:
        current_app.logger.error(f"Error getting page: {str(e)}")
        return (
            jsonify({"error": "Failed to get page"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@ocr.route("/api/ocr/page/<uuid:page_id>/image")
def get_page_image(page_id):
    """Get page image"""
    try:
        page = DocumentPage.query.filter_by(page_id=page_id).first()

        if not page:
            return jsonify({"error": "Page not found"}), HTTPStatus.NOT_FOUND

        return send_file(page.page_path)

    except Exception as e:
        current_app.logger.error(f"Error getting page image: {str(e)}")
        return (
            jsonify({"error": "Failed to get page image"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@ocr.route("/api/ocr/document/<uuid:file_id>", methods=["DELETE"])
def delete_document(file_id):
    """Delete document pages and extracted images"""
    try:
        pages = DocumentPage.query.filter_by(file_id=file_id).all()

        if not pages:
            return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND

        # Delete page images
        for page in pages:
            if os.path.exists(page.page_path):
                os.remove(page.page_path)
            db.session.delete(page)

        db.session.commit()

        return jsonify({"message": "Document deleted successfully"}), HTTPStatus.OK

    except Exception as e:
        current_app.logger.error(f"Error deleting document: {str(e)}")
        return (
            jsonify({"error": "Failed to delete document"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
