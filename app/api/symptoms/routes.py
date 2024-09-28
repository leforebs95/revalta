from flask import (
    jsonify,
    request,
)

from flask_login import login_required, current_user

from models import Symptom

from . import symptoms
from flask_app import db
from flask_app import logger


@symptoms.route("/api/addSymptom", methods=["POST"])
@login_required
def add_symptom():
    symptom_data = request.json
    symptom_name = symptom_data.get("symptomName")
    symptom_description = symptom_data.get("symptomDescription")
    symptom_duration = symptom_data.get("symptomDuration")

    logger.info(
        f"Creating symptom with {symptom_name}, {symptom_description}, {symptom_duration}"
    )
    symptom = Symptom(
        symptom_name=symptom_name,
        symptom_description=symptom_description,
        symptom_duration=symptom_duration,
        user_id=current_user.user_id,
    )
    db.session.add(symptom)
    db.session.commit()

    return jsonify(symptom.to_json()), 201


@symptoms.route("/api/symptoms", methods=["GET"])
@login_required
def get_symptoms():
    symptoms = Symptom.query.filter_by(user_id=current_user.user_id).all()
    return jsonify([symptom.to_json() for symptom in symptoms]), 200
