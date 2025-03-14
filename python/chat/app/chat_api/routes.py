from flask import jsonify, request, current_app
from http import HTTPStatus
from uuid import UUID
from typing import List, Dict

from app import db
from app.models import Conversation, Message
from utils.llm_client import AnthropicClient
from utils.vector_client import VectorClient

from . import chat


def get_llm_client():
    """Get or create LLM client from app context"""
    if not hasattr(current_app, 'llm_client'):
        current_app.llm_client = AnthropicClient()
    return current_app.llm_client


def get_vector_client(user_id: int = None):
    """Get or create vector client from app context"""
    if not hasattr(current_app, 'vector_client'):
        current_app.vector_client = VectorClient()
    if user_id is not None:
        current_app.vector_client.user_id = user_id
    return current_app.vector_client


@chat.route("/api/chat/version")
def version():
    return jsonify({"version": "1.0.0"})


@chat.route("/api/chat/conversations", methods=["POST"])
def create_conversation():
    """Create a new conversation"""
    try:
        data = request.get_json()
        if not data or "userId" not in data or "title" not in data:
            return jsonify({"error": "Missing required fields"}), HTTPStatus.BAD_REQUEST
            
        conversation = Conversation(
            user_id=data["userId"],
            title=data["title"]
        )
        db.session.add(conversation)
        db.session.commit()
        
        return jsonify(conversation.to_dict()), HTTPStatus.CREATED
        
    except Exception as e:
        current_app.logger.error(f"Error creating conversation: {str(e)}")
        return (
            jsonify({"error": "Failed to create conversation"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@chat.route("/api/chat/conversations/<uuid:conversation_id>")
def get_conversation(conversation_id):
    """Get a conversation and its messages"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        messages = [msg.to_dict() for msg in conversation.messages]
        
        response = conversation.to_dict()
        response["messages"] = messages
        return jsonify(response)
        
    except Exception as e:
        current_app.logger.error(f"Error getting conversation: {str(e)}")
        return (
            jsonify({"error": "Failed to get conversation"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@chat.route("/api/chat/conversations/<uuid:conversation_id>/messages", methods=["POST"])
def send_message(conversation_id):
    """Send a message in a conversation"""
    try:
        data = request.get_json()
        if not data or "content" not in data or "userId" not in data:
            return jsonify({"error": "Missing required fields"}), HTTPStatus.BAD_REQUEST
            
        conversation = Conversation.query.get_or_404(conversation_id)
        
        # Add user message
        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=data["content"]
        )
        db.session.add(user_message)
        
        # Get relevant context from vector DB
        vector_client = get_vector_client(user_id=data["userId"])
        context_results = vector_client.similarity_search(
            user_id=data["userId"],
            query_text=data["content"]
        )
        
        # Format context
        context = "\n\n".join(
            f"Document excerpt:\n{result['text']}"
            for result in context_results.get("results", [])
        )
        
        # Get conversation history
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in conversation.messages
        ]
        messages.append({"role": "user", "content": data["content"]})
        
        # Generate response
        llm_client = get_llm_client()
        response_text = llm_client.chat_completion(
            messages=messages,
            context=context
        )
        
        # Add assistant message
        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        db.session.add(assistant_message)
        db.session.commit()
        
        return jsonify({
            "user_message": user_message.to_dict(),
            "assistant_message": assistant_message.to_dict()
        }), HTTPStatus.CREATED
        
    except Exception as e:
        current_app.logger.error(f"Error sending message: {str(e)}")
        return (
            jsonify({"error": "Failed to send message"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@chat.route("/api/chat/conversations/<uuid:conversation_id>", methods=["DELETE"])
def delete_conversation(conversation_id):
    """Delete a conversation"""
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        db.session.delete(conversation)
        db.session.commit()
        
        return jsonify({"message": "Conversation deleted successfully"}), HTTPStatus.OK
        
    except Exception as e:
        current_app.logger.error(f"Error deleting conversation: {str(e)}")
        return (
            jsonify({"error": "Failed to delete conversation"}),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        ) 