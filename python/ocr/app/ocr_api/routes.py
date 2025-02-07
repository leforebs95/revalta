from concurrent.futures import ThreadPoolExecutor
from flask import jsonify, current_app, send_file
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


def handle_file_event(message):
    try:
        data = json.loads(message["data"])
        if data["event"] == "file_saved":
            lock_name = f"ocr_lock:{data['file_id']}"

            # Try to acquire lock with 1 second timeout
            lock = current_app.redis.set(lock_name, "locked", nx=True, ex=60)

            if not lock:
                # Another worker is processing this file
                return False
            try:
                # First create pending records for all pages
                pdf_processor = PDFProcessor(current_app.config["PAGES_LOCATION"])
                file_path = pdf_processor._download_file(
                    data["file_id"], data["filename"]
                )

                if not file_path:
                    current_app.logger.error(
                        f"Failed to download file {data['file_id']}"
                    )
                    return False

                page_count = pdf_processor.get_page_count(file_path)
                current_app.logger.info(f"Processing {page_count} pages")

                # Create pending records for each page
                pages = []
                for page_num in range(page_count):
                    page_id, page_filename = pdf_processor.extract_page(
                        file_path, page_num
                    )
                    page = DocumentPage(
                        page_id=page_id,
                        file_id=data["file_id"],
                        page_number=page_num,
                        page_path=page_filename,
                        status="pending",
                    )
                    db.session.add(page)
                    pages.append(page)
                db.session.commit()

                for page in pages:
                    current_app.logger.info(f"Proces page id: {page.page_id}")
                    process_page_task(page.file_id, page.page_number, page.page_path)

                # Now process pages in parallel
                # with ThreadPoolExecutor(max_workers=4) as executor:
                #     futures = []
                #     for page in pages:
                #         futures.append(
                #             executor.submit(
                #                 process_page_task,
                #                 page.file_id,
                #                 page.page_number,
                #                 page.page_path,
                #             )
                #         )

                return True
            finally:
                current_app.redis.delete(lock_name)
    except Exception as e:
        current_app.logger.error(f"Error processing file event: {str(e)}")
    return False


def process_page_task(file_id, page_number, page_path):
    try:

        result = processor.process_page(page_path)

        # Update the page record with results
        page = DocumentPage.query.filter_by(
            file_id=file_id, page_number=page_number
        ).first()

        current_app.logger.info(f"Processing page {page_number}: {result}")
        current_app.logger.info(f"Page Updates: {page}")

        if page:
            page.page_path = page_path
            page.text_content = result["text"]
            page.raw_data = result["raw_data"]
            page.confidence = result["confidence"]
            page.status = result["status"]
            page.error_message = result.get("error_message")
            db.session.commit()

    except Exception as e:
        current_app.logger.error(f"Error processing page {page_number}: {str(e)}")
        # Update page status to failed
        page = DocumentPage.query.filter_by(
            file_id=file_id, page_number=page_number
        ).first()
        if page:
            page.status = "failed"
            page.error_message = str(e)
            db.session.commit()


def start_listener():
    pubsub = current_app.redis.pubsub()
    pubsub.subscribe("file_events")

    for message in pubsub.listen():
        current_app.logger.info(f"Received message: {message}")
        if message["type"] == "message":
            handle_file_event(message)


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
