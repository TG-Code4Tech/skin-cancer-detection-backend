from flask import Blueprint, request, jsonify
from app.models.analysis import Analysis

# --- Variablen --------------------------------------------------------------------------------------------------------
get_all_analyses_bp = Blueprint("get_all_analyses", __name__)

# --- Route ------------------------------------------------------------------------------------------------------------
@get_all_analyses_bp.route("/get-all-analyses", methods=["GET"])
def get_all_analyses():
    user_id = request.args.get("user_id")

    if user_id is None:
        return jsonify({"error": "Keine Benutzer-ID bereitgestellt."}), 400
    
    analyses = Analysis.query.filter_by(user_id=user_id).all()

    if analyses is None:
        return jsonify({"error": "Es wurden keine Analysen für diesen Benutzer gefunden."}), 404
    
    analyses_list = [
        {
            "analysis_id": analysis.analysis_id,
            "result": analysis.result,
            "confidence_score": analysis.confidence_score,
            "user_id": analysis.user_id,
            "image_id": analysis.image_id,
        } for analysis in analyses

    ]

    return jsonify(analyses_list), 200
