from flask import Blueprint, request, jsonify

image_bp = Blueprint('images', __name__)

@image_bp.route('/upload', methods=['POST'])
def upload_image():
    # Hier sollte die Logik für das Hochladen und Verarbeiten von Bildern stehen
    file = request.files.get('file')
    if file:
        # Hier kann die Bildverarbeitung integriert werden
        return jsonify({"message": "Image uploaded successfully"}), 200
    else:
        return jsonify({"error": "No file provided"}), 400
