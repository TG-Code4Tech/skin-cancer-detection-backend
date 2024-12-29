import re
from app import db
from flask import jsonify, make_response
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.utils.enums import Theme

class UserService:
    # --- Benutzerdaten abrufen ----------------------------------------------------------------------------------------
    def get_user_data(user_id):
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        user_data = {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "email": user.email,
            "theme": user.theme
        }

        return jsonify(user_data), 200

    # --- Benutzer löschen ---------------------------------------------------------------------------------------------
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        db.session.delete(user)
        db.session.commit()

        response = make_response(jsonify({
            "message": "Account erfolgreich gelöscht.",
        }), 200)

        response.delete_cookie("jwt_access_token")

        return response

    # --- Benutzer registrieren ----------------------------------------------------------------------------------------
    @staticmethod
    def register_user(username, email, password, password_confirmation, first_name, last_name):
        is_username_valid = UserService.validate_input(username)
        is_email_valid, email_validation_message = UserService.validate_email(email)
        is_password_valid, password_validation_message = UserService.validate_password(password)
        passwords_match = UserService.check_matching_passwords(password, password_confirmation)
        is_first_name_valid = UserService.validate_input(first_name)
        is_last_name_valid = UserService.validate_input(last_name)

        if not is_username_valid:
            return jsonify({
                "check": "backend_username",
                "error": "Bitte einen Benutzernamen angeben."
            }), 400

        username_already_exists = User.query.filter_by(username=username).first()

        if username_already_exists:
            return jsonify({
                "check": "backend_username",
                "error": "Benutzername bereits vergeben."
            }), 400
        
        if not is_email_valid:
            return jsonify({
                "check": "backend_email",
                "error": email_validation_message
            }), 400
        
        email_already_exists = User.query.filter_by(email=email).first()

        if email_already_exists:
            return jsonify({
                "check": "backend_email",
                "error": "Email-Adresse bereits vergeben."
            }), 400
        
        if not is_password_valid:
            return jsonify({
                "check": "backend_password",
                "error": password_validation_message
            }), 400
        
        if not passwords_match:
            return jsonify({
                "check": "backend_password_confirmation",
                "error": "Passwörter stimmen nicht überein."
            }), 400
        
        if not is_first_name_valid:
            return jsonify({
                "check": "backend_first_name",
                "error": "Bitte einen Vornamen angeben."
            }), 400
        
        if not is_last_name_valid:
            return jsonify({
                "check": "backend_last_name",
                "error": "Bitte einen Nachnamen angeben."
            }), 400
        
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

        # JWT erstellen
        jwt_access_token = create_access_token(identity=str(new_user.user_id))

        return jsonify({
            "message": "Benutzer wurde erfolgreich registriert.", 
            "jwt_access_token": jwt_access_token,
            "user_id": new_user.user_id,
            "username": new_user.username,
            "email": new_user.email,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }), 201
    
    # --- E-Mail-Adresse ändern ----------------------------------------------------------------------------------------
    @staticmethod
    def update_email(user_id, email):
        user = User.query.get(user_id)
        is_email_valid, message = UserService.validate_email(email)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        if not is_email_valid:
            return jsonify({
                "check": "backend_email",
                "error": message
            }), 400
        
        email_already_exists = User.query.filter_by(email=email).first()

        if email_already_exists:
            return jsonify({
                "check": "backend_email",
                "error": "E-Mail-Adresse bereits vergeben."
            }), 400
        
        user.email = email
        db.session.commit()

        return jsonify({
            "message": f"E-Mail-Adresse wurde erfolgreich zu '{email}' geändert.",
            "email": user.email
        }), 200
    
    # --- Vorname ändern -----------------------------------------------------------------------------------------------
    @staticmethod
    def update_first_name(user_id, first_name):
        user = User.query.get(user_id)
        is_first_name_valid = UserService.validate_input(first_name)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        if not is_first_name_valid:
            return jsonify({
                "check": "backend_first_name",
                "error": "Kein Vorname übermittelt."
            }), 400
        
        user.first_name = first_name
        db.session.commit()

        return jsonify({
            "message": f"Vorname wurde erfolgreich zu '{first_name}' geändert.",
            "first_name": user.first_name
        }), 200
    
    # --- Nachname ändern ----------------------------------------------------------------------------------------------
    @staticmethod
    def update_last_name(user_id, last_name):
        user = User.query.get(user_id)
        is_last_name_valid = UserService.validate_input(last_name)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        if not is_last_name_valid:
            return jsonify({
                "check": "backend_last_name",
                "error": "Kein Nachname übermittelt."
            }), 400
        
        user.last_name = last_name
        db.session.commit()

        return jsonify({
            "message": f"Nachname wurde erfolgreich zu '{last_name}' geändert.",
            "last_name": user.last_name
        }), 200
    
    # --- Passwort ändern ----------------------------------------------------------------------------------------------
    @staticmethod
    def update_password(user_id, current_password, password, password_confirmation):
        user = User.query.get(user_id)
        is_password_valid, message = UserService.validate_password(password)
        matching_passwords = UserService.check_matching_passwords(password, password_confirmation)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        if not check_password_hash(user.password, current_password):
            return jsonify({
                "check": "backend_current_password",
                "error": "Falsches aktuelles Passwort."
            }), 400
        
        if not is_password_valid:
            return jsonify({
                "check": "backend_password",
                "error": message
            }), 400
        
        if not matching_passwords:
            return jsonify({
                "check": "backend_password_confirmation",
                "error": "Die Passwörter stimmen nicht überein."
            }), 400
        
        # Prüfen, ob das neue Passwort mit dem aktuellen Passwort übereinstimmt
        if check_password_hash(user.password, password):
            return jsonify({
                "check": "backend_password",
                "error": "Das neue Passwort darf nicht mit dem alten Passwort übereinstimmen."
            }), 400
        
        # Passwort hashen
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        user.password = hashed_password
        db.session.commit()

        return jsonify({
            "message": f"Passwort wurde erfolgreich geändert.",
        }), 200
    
    # --- Theme ändern -------------------------------------------------------------------------------------------------
    @staticmethod
    def update_theme(user_id, theme):
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404

        if theme not in [theme.value for theme in Theme]:
            return jsonify({"error": "Ungültiges Theme. Erlaubte Werte: 'light' oder 'dark'."}), 400

        user.theme = theme
        db.session.commit()

        return jsonify({
            "message": f"Theme wurde erfolgreich auf '{theme}' gesetzt.",
            "theme": user.theme
        }), 200
    
    # --- Benutzername ändern ------------------------------------------------------------------------------------------
    @staticmethod
    def update_username(user_id, username):
        user = User.query.get(user_id)
        is_username_valid = UserService.validate_input(username)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        if not is_username_valid:
            return jsonify({"error": "Kein Benutzername übermittelt."}), 400
    
        # Prüfen, ob bereits ein Benutzer mit dem Benutzername existiert
        username_already_exists = User.query.filter_by(username=username).first()

        if username_already_exists:
            return jsonify({"error": "Benutzername bereits vergeben."}), 400

        user.username = username
        db.session.commit()

        return jsonify({
            "message": f"Benutzername wurde erfolgreich zu '{username}' geändert.",
            "username": user.username
        }), 200
    
    # --- Auf leere Eingaben prüfen ------------------------------------------------------------------------------------
    @staticmethod
    def validate_input(input):
        if not input or not isinstance(input, str) or input.strip() == "":
            return False
        
        return True
    
    # --- Validierung der E-Mail-Adresse -------------------------------------------------------------------------------
    @staticmethod
    def validate_email(email):
        is_valid = True
        message = None
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        is_email_given = UserService.validate_input(email)
        is_email_valid = bool(re.match(regex, email))

        if not is_email_given or not is_email_valid:
            is_valid = False
            message = "Bitte eine gültige E-Mail-Adresse angeben."

        return is_valid, message

    # --- Validierung des Passworts ------------------------------------------------------------------------------------
    @staticmethod
    def validate_password(password):
        is_valid = True
        message = None

        # Prüfen, ob ein (leeres) Passwort angegeben wurde
        is_password_given = UserService.validate_input(password)
        if not is_password_given:
            is_valid = False
            message = "Bitte ein gültiges Passwort angeben."

            return is_valid, message
        
        # Prüfen, ob das Passwort aus mindestens 8 Zeichen besteht
        if len(password) < 8:
            is_valid = False
            message = "Das Passwort muss aus mindestens 8 Zeichen bestehen."

            return is_valid, message
        
        # Prüfen, ob das Passwort mindestens einen Großbuchtsaben enthält
        if not re.search(r"[A-Z]", password):
            is_valid = False
            message = "Das Passwort muss mindestens einen Großbuchstaben enthalten."

            return is_valid, message
        
        # Prüfen, ob das Passwort mindestens einen Kleinbuchstaben enthält
        if not re.search(r"[a-z]", password):
            is_valid = False
            message = "Das Passwort muss mindestens einen Kleinbuchstaben enthalten."

            return is_valid, message
        
        # Prüfen, ob das Passwort mindestens eine Zahl enthält
        if not re.search(r"\d", password):
            is_valid = False
            message = "Das Passwort muss mindestens eine Zahl enthalten."

            return is_valid, message
        
        # Prüfen, ob das Passwort mindestens eins der erlaubten Sonderzeichen enthält
        if not re.search(r"[@$!%*?&#<>|_-]", password):
            is_valid = False
            message = "Das Passwort muss mindestens eines der folgenden Sonderzeichen enthalten: @$!%*?&#<>|_-."

            return is_valid, message
        
        # Prüfen, ob das Passwort ein ungültiges Sonderzeichen enthält
        if not re.search(r"^[a-zA-Z0-9@$!%*?&#<>|_-]*$", password):
            is_valid = False
            message = "Das Passwort darf nur die folgenden Sonderzeichen enthalten: @$!%*?&#<>|_-."
        
        return is_valid, message
    
    # --- Validierung der Passwortbestätigung --------------------------------------------------------------------------
    @staticmethod
    def check_matching_passwords(password, password_confirmation):
        return password == password_confirmation
        