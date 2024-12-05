from app import db
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.utils.enums import Theme

update_theme_bp = Blueprint("update_theme", __name__)

@update_theme_bp.route("/update-theme", methods=["PUT"])
@jwt_required()
def update_theme():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

    new_theme = request.form.get("theme")

    if new_theme not in [theme.value for theme in Theme]:
        return jsonify({"error": "Ungültiges Theme. Erlaubte Werte: 'light' oder 'dark'."}), 400

    user.theme = new_theme
    db.session.commit()

    return jsonify({
        "message": f"Theme wurde erfolgreich auf '{new_theme}' gesetzt.",
        "theme": user.theme
    }), 200
