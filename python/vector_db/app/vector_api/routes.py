from flask import jsonify, request, current_app
from http import HTTPStatus
from uuid import UUID

from app import logger
from app.models import db, Document, DocumentChunk
from . import vector
from utils.chunking import DocumentChunker
from utils.embeddings import get_embedder
from utils.db.context import user_context

# Initialize services
chunker = DocumentChunker()
embedder = get_embedder()


@vector.route("/api/vector/version")
def version():
    return jsonify({"version": "1.0.0"})


@vector.route("/api/vector/document", methods=["POST"])
def insert_document():
    try:
        # Get POST data
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST

        user_id = data.get("userId")
        text = data.get("text")

        if not user_id or not text:
            return jsonify({"error": "Missing required fields"}), HTTPStatus.BAD_REQUEST

        # Set user_id for this request
        current_app.vector_db.user_id = user_id

        # Process document within user context
        with user_context(user_id):
            # Process document
            chunks = chunker.chunk_document(text)
            chunk_data = []

            for chunk in chunks:
                embedding = embedder.embed_text(chunk.text)
                chunk_data.append(
                    {
                        "text": chunk.text,
                        "seq_number": chunk.seq_number,
                        "embedding": embedding,
                        "metadata": chunk.metadata,
                    }
                )

            # Insert into DB
            doc_id = current_app.vector_db.insert_document(text, chunk_data)

            return (
                jsonify({"documentId": str(doc_id), "numChunks": len(chunks)}),
                HTTPStatus.CREATED,
            )

    except Exception as e:
        logger.error(f"Error inserting document: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@vector.route("/api/vector/search/similarity", methods=["POST"])
def similarity_search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST

        user_id = data.get("userId")
        query_text = data.get("queryText")
        k = data.get("k", 5)
        score_threshold = data.get("scoreThreshold")

        if not user_id or not query_text:
            return jsonify({"error": "Missing required fields"}), HTTPStatus.BAD_REQUEST

        # Set user_id for this request
        current_app.vector_db.user_id = user_id

        # Get embeddings and search within user context
        with user_context(user_id):
            query_embedding = embedder.embed_text(query_text)
            results = current_app.vector_db.similarity_search(
                query_embedding, k=k, score_threshold=score_threshold
            )

            return jsonify({"results": results}), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error in similarity search: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@vector.route("/api/vector/search/keyword", methods=["POST"])
def keyword_search():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), HTTPStatus.BAD_REQUEST

        user_id = data.get("userId")
        keyword = data.get("keyword")
        k = data.get("k", 5)

        if not user_id or not keyword:
            return jsonify({"error": "Missing required fields"}), HTTPStatus.BAD_REQUEST

        # Set user_id for this request
        current_app.vector_db.user_id = user_id

        # Search within user context
        with user_context(user_id):
            results = current_app.vector_db.keyword_search(keyword, k=k)
            return jsonify({"results": results}), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error in keyword search: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@vector.route("/api/vector/document/<uuid:document_id>")
def get_document(document_id):
    try:
        user_id = request.args.get("userId")
        if not user_id:
            return (
                jsonify({"error": "Missing userId parameter"}),
                HTTPStatus.BAD_REQUEST,
            )

        # Set user_id for this request
        current_app.vector_db.user_id = int(user_id)

        # Get document within user context
        with user_context(int(user_id)):
            doc = current_app.vector_db.get_document(document_id)

            if not doc:
                return jsonify({"error": "Document not found"}), HTTPStatus.NOT_FOUND

            return jsonify(doc), HTTPStatus.OK

    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        return (
            jsonify({"error": "An unexpected error occurred"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )
