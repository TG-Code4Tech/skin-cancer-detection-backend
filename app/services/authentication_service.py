from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.models.user import User

class AuthenticationService:

    @staticmethod
    def login_user(username_or_email, password):
        is_username_or_email_valid = AuthenticationService.validate_input(username_or_email)
        is_password_valid = AuthenticationService.validate_input(password)

        if not is_username_or_email_valid:
            return jsonify({"error": "Bitte einen gültigen Benutzernamen oder eine gültige E-Mail-Adresse angeben."}), 400

        if not is_password_valid:
            return jsonify({"error": "Bitte ein gültiges Passwort angeben."}), 400
        
        # Prüfen, ob ein Benutzer mit dem Benutzernamen oder der E-Mail exisitiert
        user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

        if user is None:
            return jsonify({"error": "Benutzername oder E-Mail-Adresse ist ungültig."}), 400
        
        # Passwort prüfen
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Falsches Passwort."}), 400
    
        # JWT erstellen
        jwt_access_token = create_access_token(identity=str(user.user_id))

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

    @staticmethod
    def validate_input(input):
        if not input or not isinstance(input, str) or input.strip() == "":
            return False
        
        return True
    