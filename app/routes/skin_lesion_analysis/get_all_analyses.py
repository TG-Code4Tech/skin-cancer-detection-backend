from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.analysis_service import AnalysisService

get_all_analyses_bp = Blueprint("get_all_analyses", __name__)

@get_all_analyses_bp.route("/get-all-analyses", methods=["GET"])
@jwt_required()
def get_all_analyses():
    user_id = get_jwt_identity()
    response = AnalysisService.get_all_analyses(user_id)
    
    return response
