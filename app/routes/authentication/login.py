from app import db
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user import User

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    username_or_email = request.form.get("username_or_email")
    password = request.form.get("password")

    if username_or_email is None or password is None:
        return jsonify({"error": "Bitte alle erforderlichen Felder ausfüllen."}), 400
    
    # Prüfen, ob ein Benutzer mit dem Benutzernamen oder der E-Mail exisitiert
    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user is None:
        return jsonify({"error": "Benutzername oder E-Mail-Adresse ist ungültig."}), 400
    
    # Passwort prüfen
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Falsches Passwort."}), 400
    
    # JWT erstellen
    jwt_access_token = create_access_token(identity=user.user_id)

    response = make_response(jsonify({
        "message": "Erfolgreich angemeldet.",
        "jwt_access_token": jwt_access_token,
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name
    }), 200)

    response.set_cookie("jwt_access_token", jwt_access_token, httponly=True, secure=False, samesite="Strict")

    return response
    