from app import db
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from app.models.user import User

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    
    if username is None or email is None or password is None or first_name is None or last_name is None:
        return jsonify({"error": "Bitte alle erforderlichen Felder ausfüllen."}), 400
    
    # Prüfen, ob bereits ein Benutzer mit dem Benutzername oder der E-Mail existiert
    username_already_exists = User.query.filter_by(username=username).first()

    if username_already_exists:
        return jsonify({"error": "Benutzername bereits vergeben."}), 400
    
    email_already_exists = User.query.filter_by(email=email).first()

    if email_already_exists:
        return jsonify({"error": "Email-Adresse bereits vergeben."}), 400
    
    # Passwort hashen
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    # Neuen Benutzer anlegen
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Benutzer wurde erfolgreich registriert.", 
        "user_id": new_user.user_id,
        "username": new_user.username,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name
    }), 201
