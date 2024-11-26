import os
from app import db
from app.models.image import Image
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

# --- Variablen --------------------------------------------------------------------------------------------------------
upload_skin_lesion_bp = Blueprint("upload_skin_lesion", __name__)

# --- Hilfsfunktionen --------------------------------------------------------------------------------------------------
def save_file_in_uploads_directory(file, user_id):
    # Uploads Verzeichnis erstellen
    uploads_directory = os.path.join(os.path.dirname(__file__), f"../../uploads/{user_id}")
    os.makedirs(uploads_directory, exist_ok=True)

    # Datei speichern
    filename = secure_filename(file.filename)
    uploads_path = os.path.join(uploads_directory, filename)
    
    file.save(uploads_path)

    return os.path.join("uploads", str(user_id), filename)

# --- Route ------------------------------------------------------------------------------------------------------------
@upload_skin_lesion_bp.route("/upload-skin-lesion", methods=["POST"])
def upload_skin_lesion():
    file = request.files["skin-lesion-image"]

    if file is None or file.filename == "":
        return jsonify({"error": "Keine Hautläsion bereitgestellt."})
    
    # Bildpfad in Datenbank speichern
    user_id = 1  # TODO: Das muss später über den Request übergeben werden --> SCD-20

    image_path = save_file_in_uploads_directory(file, user_id)

    image = Image(
        image=image_path,
        user_id=user_id
    )

    db.session.add(image)
    db.session.commit()

    return jsonify({"message": "Das Bild wurde erfolgreich gespeichert."}), 201
