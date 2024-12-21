from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.skin_cancer_detection_service import SkinCancerDetectionService

upload_skin_lesion_bp = Blueprint("upload_skin_lesion", __name__)

@upload_skin_lesion_bp.route("/upload-skin-lesion", methods=["POST"])
@jwt_required()
def upload_skin_lesion():
    user_id = get_jwt_identity()
    file = request.files["skin-lesion-image"]   
    service = SkinCancerDetectionService()
    response = service.upload_skin_lesion(user_id, file)

    return response
    