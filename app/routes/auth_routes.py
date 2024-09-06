from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    # Hier sollte die Logik für die Authentifizierung stehen
    data = request.json
    # Beispielhafte Rückgabe
    return jsonify({"message": "Login successful", "data": data}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    # Hier sollte die Logik für die Registrierung stehen
    data = request.json
    # Beispielhafte Rückgabe
    return jsonify({"message": "Registration successful", "data": data}), 201
