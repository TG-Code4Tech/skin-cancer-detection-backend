import os
import shutil
import numpy as np
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models.analysis import Analysis
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# --- Variablen --------------------------------------------------------------------------------------------------------
analyze_skin_lesion_bp = Blueprint("analyze_skin_lesion", __name__)
skin_cancer_detection_model_path = os.path.join(os.path.dirname(__file__), "../../../model/skin_cancer_detection_model.keras")
model = load_model(skin_cancer_detection_model_path)

# --- Hilfsfunktionen --------------------------------------------------------------------------------------------------
def save_file_temporarily(file):
    # Temporäres Verzeichnis erstellen
    temp_directory = os.path.join(os.path.dirname(__file__), '../../temp')
    os.makedirs(temp_directory, exist_ok=True)

    # Datei speichern
    filename = secure_filename(file.filename)
    temp_path = os.path.join(temp_directory, filename)
    file.save(temp_path)

    return temp_path, temp_directory

def prepare_image(image_path):
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image / 255.0

    return image

def remove_temp_directory(temp_directory):
    if os.path.exists(temp_directory):
        shutil.rmtree(temp_directory)

# --- Route ------------------------------------------------------------------------------------------------------------
@analyze_skin_lesion_bp.route("/analyze-skin-lesion", methods=["POST"])
def analyze_skin_lesion():
    file = request.files["skin-lesion-image"]

    if file is None or file.filename == "":
        return jsonify({"error": "Keine Hautläsion bereitgestellt."})
    
    image_path, temp_directory = save_file_temporarily(file)

    try:
        image = prepare_image(image_path)
        prediction = model.predict(image)
        result = "malignant" if prediction[0][0] > 0.5 else "benign"
        confidence_score = float(prediction[0][0])

        # Analyse in Datenbank speichern
        user_id = 1  # TODO: Das muss später über den Request übergeben werden --> SCD-20
        image_id = 1  # TODO: Das muss später über den Request übergeben werden --> SCD-18

        analysis = Analysis(
            result=result,
            confidence_score=confidence_score,
            user_id=user_id,
            image_id=image_id
        )

        db.session.add(analysis)
        db.session.commit()

        return jsonify({"prediction": result, "confidence": confidence_score})
    
    finally:
        remove_temp_directory(temp_directory)
        