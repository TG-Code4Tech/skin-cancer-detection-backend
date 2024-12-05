from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

update_email_bp = Blueprint("update_email", __name__)

@update_email_bp.route("/update-email", methods=["PUT"])
@jwt_required()
def update_email():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

    new_email = request.form.get("email")

    if new_email is None:
        return jsonify({"error": "Keine E-Mail-Adresse übermittelt."}), 400
    
    # Prüfen, ob bereits ein Benutzer mit der E-Mail-Adresse existiert
    email_already_exists = User.query.filter_by(email=new_email).first()

    if email_already_exists:
        return jsonify({"error": "E-Mail-Adresse bereits vergeben."}), 400

    user.email = new_email
    db.session.commit()

    return jsonify({
        "message": f"E-Mail-Adresse wurde erfolgreich zu '{new_email}' geändert.",
        "username": user.email
    }), 200
