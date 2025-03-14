import json
from uuid import UUID
from flask import jsonify, request, current_app, send_file, g
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized
from http import HTTPStatus
import os

from . import uploads
from app import logger
from app.models import db, Upload
from utils.file_storage import LocalFileStorage
from utils.validation import validate_file
from app.middleware.auth import jwt_required


@uploads.route("/api/uploads/version", methods=["GET"])
def version():
    return jsonify({"version": "0.0.1"})


@uploads.route("/api/uploads/upload", methods=["POST"])
@jwt_required
def upload_file():
    try:
        # Validate request
        if "file" not in request.files:
            raise BadRequest("No file provided")

        uploaded_file = request.files["file"]

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

        # Create database record using user_id from JWT
        file_record = Upload(
            user_id=g.user_id,
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
        return jsonify({"error": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR


@uploads.route("/api/uploads", methods=["GET"])
@jwt_required
def get_user_uploads():
    try:
        uploads = Upload.query.filter_by(user_id=g.user_id, is_deleted=False).all()
        return jsonify([upload.to_json() for upload in uploads])

    except Exception as e:
        logger.error(f"Error retrieving uploads: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR


@uploads.route("/api/uploads/<uuid:file_id>/download", methods=["GET"])
@jwt_required
def download_file(file_id):
    try:
        file_record = Upload.query.get(file_id)
        if not file_record or file_record.is_deleted:
            raise NotFound("File not found")

        # Verify ownership using user_id from JWT
        if file_record.user_id != g.user_id:
            raise Unauthorized("Access denied")

        storage = LocalFileStorage(current_app.config["UPLOAD_DIRECTORY"])
        file_obj = storage.get_file(file_record.file_path)

        if not file_obj:
            raise NotFound("File not found in storage")

        return send_file(
            file_obj,
            download_name=file_record.original_filename,
            mimetype=file_record.mime_type,
        )

    except (NotFound, Unauthorized) as e:
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        logger.error(f"File download error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR


@uploads.route("/api/uploads/<uuid:file_id>", methods=["DELETE"])
@jwt_required
def delete_file(file_id):
    try:
        file_record = Upload.query.get(file_id)
        if not file_record or file_record.is_deleted:
            raise NotFound("File not found")

        # Verify ownership using user_id from JWT
        if file_record.user_id != g.user_id:
            raise Unauthorized("Access denied")

        storage = LocalFileStorage(current_app.config["UPLOAD_DIRECTORY"])
        if storage.delete_file(file_record.file_path):
            file_record.soft_delete()
            db.session.commit()
            return "", HTTPStatus.NO_CONTENT
        else:
            raise BadRequest("Failed to delete file")

    except (NotFound, BadRequest, Unauthorized) as e:
        return jsonify({"error": str(e)}), e.code
    except Exception as e:
        logger.error(f"File deletion error: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), HTTPStatus.INTERNAL_SERVER_ERROR
