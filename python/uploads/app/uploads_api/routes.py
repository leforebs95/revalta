import json
from uuid import UUID
from flask import jsonify, request, current_app, send_file
from werkzeug.exceptions import BadRequest, NotFound
from http import HTTPStatus
import os

from . import uploads
from app import logger
from app.models import db, Upload
from utils.file_storage import LocalFileStorage
from utils.validation import validate_file


@uploads.route("/api/uploads/version", methods=["GET"])
def version():
    return jsonify({"version": "0.0.1"})


@uploads.route("/api/uploads/upload", methods=["POST"])
def upload_file():
    try:
        # Validate request
        if "file" not in request.uploads:
            raise BadRequest("No file provided")

        uploaded_file = request.uploads["file"]
        user_id = request.form.get("userId")

        if not user_id:
            raise BadRequest("User ID is required")

        # Validate file
        is_valid, error_message = validate_file(uploaded_file)
        if not is_valid:
            raise BadRequest(error_message)

        # Initialize storage
        storage = LocalFileStorage(current_app.config["UPLOAD_DIRECTORY"])

        # Save file
        success, stored_filename, file_path = storage.save_file(
            uploaded_file, uploaded_file.filename
        )

        if not success:
            raise BadRequest("Failed to save file")

        # Create database record
        file_record = Upload(
            user_id=user_id,
            filename=stored_filename,
            original_filename=uploaded_file.filename,
            file_path=file_path,
            file_size=os.path.getsize(file_path),
            mime_type=uploaded_file.mimetype,
        )

        db.session.add(file_record)
        db.session.commit()

        return jsonify(file_record.to_json()), HTTPStatus.CREATED

    except BadRequest as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    except Exception as e:
        logger.error(f"File upload error: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@uploads.route("/api/uploads/<int:user_id>", methods=["GET"])
def get_user_uploads(user_id):
    try:
        uploads = Upload.query.filter_by(user_id=user_id, is_deleted=False).all()
        return jsonify([upload.to_json() for upload in uploads])

    except Exception as e:
        logger.error(f"Error retrieving uploads: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@uploads.route("/api/uploads/<uuid:file_id>/download", methods=["GET"])
def download_file(file_id):
    try:
        file_record = Upload.query.get(file_id)
        if not file_record or file_record.is_deleted:
            raise NotFound("File not found")

        storage = LocalFileStorage(current_app.config["UPLOAD_DIRECTORY"])
        file_obj = storage.get_file(file_record.file_path)

        if not file_obj:
            raise NotFound("File not found in storage")

        return send_file(
            file_obj,
            download_name=file_record.original_filename,
            mimetype=file_record.mime_type,
        )

    except NotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@uploads.route("/api/uploads/<uuid:file_id>", methods=["DELETE"])
def delete_file(file_id):
    try:
        file_record = Upload.query.get(file_id)
        if not file_record or file_record.is_deleted:
            raise NotFound("File not found")

        storage = LocalFileStorage(current_app.config["UPLOAD_DIRECTORY"])
        if storage.delete_file(file_record.file_path):
            file_record.soft_delete()
            db.session.commit()
            return "", HTTPStatus.NO_CONTENT
        else:
            raise BadRequest("Failed to delete file")

    except (NotFound, BadRequest) as e:
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        logger.error(f"File deletion error: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
