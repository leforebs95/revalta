from concurrent.futures import ThreadPoolExecutor
from flask import jsonify, current_app, send_file, request
import json
from uuid import UUID
from app.models import db, DocumentPage
from utils.ocr_processor import OCRProcessor, PDFProcessor

from . import ocr

processor = OCRProcessor()


@ocr.route("/api/ocr/version")
def version():
    return jsonify({"version": "1.0.0"})


@ocr.route("/api/ocr/pages/<uuid:file_id>")
def get_pages(file_id):
    try:
        pages = (
            DocumentPage.query.filter_by(file_id=file_id)
            .order_by(DocumentPage.page_number)
            .all()
        )
        return jsonify([page.to_dict() for page in pages])
    except Exception as e:
        current_app.logger.error(f"Error fetching pages: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/pages/<uuid:file_id>/<int:page_number>")
def get_page(file_id, page_number):
    try:
        page = DocumentPage.query.filter_by(
            file_id=file_id, page_number=page_number
        ).first()
        if not page:
            return jsonify({"error": "Page not found"}), 404

        return jsonify(page.to_dict())

    except Exception as e:
        current_app.logger.error(f"Error fetching page: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/pages/<uuid:file_id>/<int:page_number>/image")
def get_page_image(file_id, page_number):
    try:
        page = DocumentPage.query.filter_by(
            file_id=file_id, page_number=page_number
        ).first()
        if not page:
            return jsonify({"error": "Page not found"}), 404

        return send_file(page.page_path)

    except Exception as e:
        current_app.logger.error(f"Error fetching page image: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/documents/<uuid:file_id>/pages", methods=["POST"])
def create_document_pages(file_id):
    try:
        # Create pending records for all pages
        pdf_processor = PDFProcessor(current_app.config["PAGES_LOCATION"])
        file_path = pdf_processor._download_file(file_id)

        if not file_path:
            current_app.logger.error(f"Failed to download file {file_id}")
            return jsonify({"error": "Failed to download file"}), 500

        page_count = pdf_processor.get_page_count(file_path)
        current_app.logger.info(f"Processing {page_count} pages")

        # Create pending records for each page
        pages = []
        for page_num in range(page_count):
            page_id, page_filename = pdf_processor.extract_page(file_path, page_num)
            page = DocumentPage(
                page_id=page_id,
                file_id=file_id,
                page_number=page_num,
                page_path=page_filename,
                status="pending",
            )
            db.session.add(page)
            pages.append(page)

        db.session.commit()

        return jsonify({"pages": [page.to_dict() for page in pages]}), 201

    except Exception as e:
        current_app.logger.error(f"Error creating document pages: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/documents/<uuid:file_id>/process", methods=["POST"])
def process_document_pages(file_id):
    try:
        # Get page range from request params if provided
        start_page = request.args.get("start_page", type=int)
        end_page = request.args.get("end_page", type=int)

        # Query pages to process
        query = DocumentPage.query.filter_by(file_id=file_id, status="pending")
        if start_page is not None:
            query = query.filter(DocumentPage.page_number >= start_page)
        if end_page is not None:
            query = query.filter(DocumentPage.page_number <= end_page)

        pages = query.order_by(DocumentPage.page_number).all()

        if not pages:
            return jsonify({"message": "No pending pages found"}), 404

        # Process each page
        for page in pages:
            result = processor.process_page(page.page_path)

            page.text_content = result["text"]
            page.raw_data = result["raw_data"]
            page.confidence = result["confidence"]
            page.status = result["status"]
            page.error_message = result.get("error_message")

            db.session.commit()

        return jsonify({"processed_pages": [page.to_dict() for page in pages]})

    except Exception as e:
        current_app.logger.error(f"Error processing pages: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/pages/<uuid:file_id>/<int:page_number>/retry", methods=["POST"])
def retry_page(file_id, page_number):
    try:
        page = DocumentPage.query.filter_by(
            file_id=file_id, page_number=page_number
        ).first()
        if not page:
            return jsonify({"error": "Page not found"}), 404

        success = processor.retry_page(page)
        db.session.commit()

        return jsonify(page.to_dict())

    except Exception as e:
        current_app.logger.error(f"Error retrying page: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/pages/<uuid:file_id>/retry", methods=["POST"])
def retry_failed_pages(file_id):
    try:
        failed_pages = DocumentPage.query.filter_by(
            file_id=file_id, status="failed"
        ).all()
        if not failed_pages:
            return jsonify({"error": "No failed pages found"}), 404

        results = []
        for page in failed_pages:
            success = processor.retry_page(page)
            results.append({"page_number": page.page_number, "success": success})

        db.session.commit()

        return jsonify({"file_id": file_id, "results": results})

    except Exception as e:
        current_app.logger.error(f"Error retrying pages: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/status/<uuid:file_id>")
def get_status(file_id):
    try:
        pages = DocumentPage.query.filter_by(file_id=file_id).all()
        if not pages:
            return jsonify({"error": "File not found"}), 404

        status_counts = {
            "total": len(pages),
            "complete": sum(1 for p in pages if p.status == "complete"),
            "failed": sum(1 for p in pages if p.status == "failed"),
            "pending": sum(1 for p in pages if p.status == "pending"),
        }
        current_app.logger.info(f"Status counts: {status_counts}")

        return jsonify({"file_id": file_id, "status": status_counts})

    except Exception as e:
        current_app.logger.error(f"Error getting status: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/pages/<uuid:file_id>", methods=["DELETE"])
def delete_pages(file_id):
    try:
        pages = DocumentPage.query.filter_by(file_id=file_id).all()
        if not pages:
            return jsonify({"error": "File not found"}), 404

        for page in pages:
            db.session.delete(page)
        db.session.commit()

        return jsonify({"message": "All pages deleted successfully"})

    except Exception as e:
        current_app.logger.error(f"Error deleting pages: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@ocr.route("/api/ocr/pages/<uuid:file_id>/<int:page_number>", methods=["DELETE"])
def delete_page(file_id, page_number):
    try:
        page = DocumentPage.query.filter_by(
            file_id=file_id, page_number=page_number
        ).first()
        if not page:
            return jsonify({"error": "Page not found"}), 404

        db.session.delete(page)

        # Update page numbers for pages greater than the deleted page
        pages_to_update = DocumentPage.query.filter(
            DocumentPage.file_id == file_id, DocumentPage.page_number > page_number
        ).all()

        for p in pages_to_update:
            p.page_number -= 1

        db.session.commit()

        return jsonify({"message": "Page deleted successfully"})

    except Exception as e:
        current_app.logger.error(f"Error deleting page: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500
