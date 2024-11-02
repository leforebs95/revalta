from flask import Blueprint, request, jsonify
from models import db, Waitlist

waitlist_bp = Blueprint("waitlist", __name__)


@waitlist_bp.route("/api/waitlist", methods=["POST"])
def add_to_waitlist():
    data = request.get_json()
    new_entry = Waitlist(**data)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Added to waitlist"}), 201


@waitlist_bp.route("/api/waitlist/<int:id>", methods=["GET"])
def get_from_waitlist(id):
    entry = Waitlist.query.get_or_404(id)
    return jsonify(entry.to_dict()), 200


@waitlist_bp.route("/api/waitlist/<int:id>", methods=["DELETE"])
def delete_from_waitlist(id):
    entry = Waitlist.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Deleted from waitlist"}), 200
