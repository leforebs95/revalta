from flask import jsonify, request
from flask_login import (
    login_required,
    login_user,
    current_user,
    logout_user,
)

from flask_app import db
from flask_app import logger
from flask_app import bcrypt

from . import lab_results
from models import LabResult


@lab_results.route("/api/addResult", methods=["POST"])
def add_result():
    result_data = request.json
    logger.info(f"result_data: {result_data}")
    result = LabResult(
        name=result_data.get("name"),
        description=result_data.get("description"),
        s3_location=result_data.get("s3Location"),
        user_id=current_user.get_id(),
    )
    # logger.info(f"result: {result}")
    # db.session.add(result)
    # db.session.commit()

    return jsonify(result.to_json()), 201
