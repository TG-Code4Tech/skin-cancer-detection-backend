from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

update_last_name_bp = Blueprint("update_last_name", __name__)

@update_last_name_bp.route("/update-last-name", methods=["PUT"])
@jwt_required()
def update_last_name():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

    new_last_name = request.form.get("last_name")

    if new_last_name is None:
        return jsonify({"error": "Kein Nachname übermittelt."}), 400

    user.last_name = new_last_name
    db.session.commit()

    return jsonify({
        "message": f"Nachname wurde erfolgreich zu '{new_last_name}' geändert.",
        "last_name": user.last_name
    }), 200
