from app.services.skin_cancer_detection_service import SkinCancerDetectionService
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analysis_service import AnalysisService

get_skin_lesion_bp = Blueprint("get_skin_lesion", __name__)

@get_skin_lesion_bp.route("/get-skin-lesion", methods=["GET"])
@jwt_required()
def get_skin_lesion():
    user_id = get_jwt_identity()
    image_id = request.args.get("image_id")
    service = SkinCancerDetectionService()
    response = service.get_skin_lesion(user_id, image_id)
    
    return response
