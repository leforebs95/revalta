# app/api/document_handler/routes.py
from flask import request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import uuid
import boto3

from models import Document
from flask_app import logger
from extensions import db
from utils.document_handler import DocumentHandler
from . import documents


@documents.route("/api/documents/presign", methods=["POST"])
@login_required
def get_presigned_url():
    data = request.get_json()
    filename = secure_filename(data["filename"])
    content_type = data["contentType"]

    s3_key = f"users/{current_user.user_id}/documents/{uuid.uuid4()}/{filename}"
    s3_client = boto3.client("s3")
    presigned_url = s3_client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": "nivalta-health",
            "Key": s3_key,
            "ContentType": content_type,
        },
        ExpiresIn=3600,
    )

    logger.info(f"Generated presigned URL for {s3_key}")
    return jsonify({"uploadUrl": presigned_url, "s3_key": s3_key})


@documents.route("/api/documents/complete", methods=["POST"])
@login_required
def complete_upload():
    data = request.get_json()
    s3_key = data["s3_key"]
    filename = data["filename"]
    content_type = data["contentType"]

    handler = DocumentHandler(db)
    document = handler.process_document(
        s3_key, filename, content_type, current_user.user_id
    )

    return jsonify(document.to_json())


@documents.route("/api/documents", methods=["GET"])
@login_required
def get_documents():
    documents = Document.query.filter_by(
        user_id=current_user.user_id, is_deleted=False
    ).all()
    docs_json = [doc.to_json() for doc in documents]
    return jsonify({"documents": docs_json})


@documents.route("/api/documents/<int:document_id>", methods=["DELETE"])
@login_required
def delete_document(document_id):
    document = Document.query.filter_by(
        document_id=document_id, user_id=current_user.user_id
    ).first_or_404()

    document.is_deleted = True
    db.session.commit()

    return jsonify({"message": "Document deleted"})
