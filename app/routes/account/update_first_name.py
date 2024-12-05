from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

update_first_name_bp = Blueprint("update_first_name", __name__)

@update_first_name_bp.route("/update-first-name", methods=["PUT"])
@jwt_required()
def update_first_name():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

    new_first_name = request.form.get("first_name")

    if new_first_name is None:
        return jsonify({"error": "Kein Vorname übermittelt."}), 400

    user.first_name = new_first_name
    db.session.commit()

    return jsonify({
        "message": f"Vorname wurde erfolgreich zu '{new_first_name}' geändert.",
        "first_name": user.first_name
    }), 200
