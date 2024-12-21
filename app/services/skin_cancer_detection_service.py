import os
import mimetypes
from app import db
from flask import jsonify
from tensorflow.keras.models import load_model
from app.models.analysis import Analysis
from app.models.image import Image
from app.utils.utils import save_file_temporarily, prepare_image, remove_temp_directory, save_file_in_uploads_directory

class SkinCancerDetectionService:

    def __init__(self):
        # Modell laden
        self.skin_cancer_detection_model_path = os.path.join(os.path.dirname(__file__), "../../model/skin_cancer_detection_model.keras")
        self.skin_cancer_detection_model = load_model(self.skin_cancer_detection_model_path)

    # --- Hautläsion analysieren ---------------------------------------------------------------------------------------
    def analyze_skin_lesion(self, file, user_id, image_id):
        if not file or file.filename == "":
            return jsonify({"error": "Keine Hautläsion bereitgestellt."})
    
        image_path, temp_directory = save_file_temporarily(file)

        try:
            image = prepare_image(image_path)
            prediction = self.skin_cancer_detection_model.predict(image)
            result = "malignant" if prediction[0][0] > 0.5 else "benign"
            confidence_score = float(prediction[0][0])

            # Analyse in der Datenbank speichern
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

    # --- Hautläsion hochladen -----------------------------------------------------------------------------------------
    def upload_skin_lesion(self, user_id, file):
        if not file or file.filename == "":
            return jsonify({"error": "Keine Hautläsion bereitgestellt."}), 400
        
        if not self.is_image(file):
            return jsonify({"error": "Die hochgeladene Datei ist kein gültiges Bild."}), 400

        image_path = save_file_in_uploads_directory(file, user_id)

        image = Image(
            image=image_path,
            user_id=user_id
        )

        db.session.add(image)
        db.session.commit()

        return jsonify({"message": "Das Bild wurde erfolgreich gespeichert.", "image_id": image.image_id}), 201

    # --- Prüfen, ob die Datei ein Bild ist ----------------------------------------------------------------------------
    def is_image(self, file):
        mime_type, _= mimetypes.guess_type(file.filename)

        if mime_type and mime_type.startswith("image"):
            allowed_extensions = [".jpg", ".jpeg", ".png"]
            _, ext = os.path.splitext(file.filename)

            if ext.lower() not in allowed_extensions:
                return False
            
            return True
        
        return False
    