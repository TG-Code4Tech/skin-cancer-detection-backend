import os
import mimetypes
from app import db
from app.services.analysis_service import AnalysisService
from flask import jsonify, send_file
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
            result = "bösartig" if prediction[0][0] > 0.5 else "gutartig"
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

            interpreted_confidence_score = AnalysisService.interpret_confidence(confidence_score)
            recommendation = f"Ihre Hautläsion wurde von dem Modell zu {interpreted_confidence_score}% als {result} eingestuft. Bitte konsultieren Sie unabängig von der Diagnose einen Dermatologen, um eine verbindliche Aussage zu erhalten."

            return jsonify({"prediction": result, "confidence": interpreted_confidence_score, "recommendation": recommendation})
    
        finally:
            remove_temp_directory(temp_directory)

    # --- Hautläsion hochladen -----------------------------------------------------------------------------------------
    def upload_skin_lesion(self, user_id, file):
        if not file or file.filename == "":
            return jsonify({"error": "Keine Hautläsion bereitgestellt."}), 400
        
        if not self.is_image(file):
            return jsonify({"error": "Die hochgeladene Datei ist kein gültiges Bild."}), 400

        filename = save_file_in_uploads_directory(file, user_id)

        image = Image(
            image=filename,
            user_id=user_id
        )

        db.session.add(image)
        db.session.commit()

        return jsonify({"message": "Das Bild wurde erfolgreich gespeichert.", "image_id": image.image_id}), 201
    
    # --- Hautläsion abrufen -----------------------------------------------------------------------------------------
    def get_skin_lesion(self, user_id, image_id):
        if not image_id:
            return jsonify({"error": "Keine image_id übergeben."}), 400
        
        image = Image.query.filter_by(image_id=image_id).first()

        if image is None:
            return jsonify({"error": "Es konnte kein Bild mit dieser ID gefunden werden."}), 404
        
        if str(image.user_id) != str(user_id):            
            return jsonify({"error": "Das Bild gehört nicht dem aktuellen Benutzer."}), 403
        
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        uploads_dir = os.path.join(project_root, 'uploads', str(image.user_id))
        image_path = os.path.join(uploads_dir, image.image)

        if not os.path.exists(image_path):
            return jsonify({"error": "Das Bild konnte auf dem Server nicht gefunden werden."}), 404
        
        mime_type, _ = mimetypes.guess_type(image_path)

        if not mime_type:
            return jsonify({"error": "Der MIME-Type des Bildes konnte nicht bestimmt werden."}), 415

        try:
            return send_file(image_path, mimetype=mime_type)
        except Exception as e:
            return jsonify({"error": f"Fehler beim Abrufen des Bildes: {str(e)}"}), 500

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
    