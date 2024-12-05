from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

update_password_bp = Blueprint("update_password", __name__)

@update_password_bp.route("/update-password", methods=["PUT"])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

    new_password = request.form.get("password")

    if new_password is None:
        return jsonify({"error": "Kein Passwort übermittelt."}), 400
    
    # Prüfen, ob das neue Passwort mit dem aktuellen Passwort übereinstimmt
    if check_password_hash(user.password, new_password):
        return jsonify({"error": "Das neue Passwort darf nicht mit dem alten Passwort übereinstimmen."}), 400
    
    # Passwort hashen
    hashed_password = generate_password_hash(new_password, method="pbkdf2:sha256")

    user.password = hashed_password
    db.session.commit()

    return jsonify({
        "message": f"Passwort wurde erfolgreich geändert.",
    }), 200
