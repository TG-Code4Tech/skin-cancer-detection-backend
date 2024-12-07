from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.skin_cancer_detection_service import SkinCancerDetectionService

analyze_skin_lesion_bp = Blueprint("analyze_skin_lesion", __name__)

@analyze_skin_lesion_bp.route("/analyze-skin-lesion", methods=["POST"])
@jwt_required()
def analyze_skin_lesion():
    user_id = get_jwt_identity()
    image_id = request.form.get("image_id")
    file = request.files["skin-lesion-image"]
    skin_cancer_detection_service = SkinCancerDetectionService()
    response = skin_cancer_detection_service.analyze_skin_lesion(file, user_id, image_id)
    
    return response
    