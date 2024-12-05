from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

update_username_bp = Blueprint("update_username", __name__)

@update_username_bp.route("/update-username", methods=["PUT"])
@jwt_required()
def update_username():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

    new_username = request.form.get("username")

    if new_username is None:
        return jsonify({"error": "Kein Benutzername übermittelt."}), 400
    
    # Prüfen, ob bereits ein Benutzer mit dem Benutzername existiert
    username_already_exists = User.query.filter_by(username=new_username).first()

    if username_already_exists:
        return jsonify({"error": "Benutzername bereits vergeben."}), 400

    user.username = new_username
    db.session.commit()

    return jsonify({
        "message": f"Benutzername wurde erfolgreich zu '{new_username}' geändert.",
        "username": user.username
    }), 200
