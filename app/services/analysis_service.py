from flask import jsonify
from app.models.analysis import Analysis
from app.models.user import User

class AnalysisService:

    @staticmethod
    def get_all_analyses(user_id):
        user = User.query.get(user_id)

        if user is None:
            return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
        
        analyses = Analysis.query.filter_by(user_id=user_id).all()

        if analyses is None:
            return jsonify({"error": "Es wurden keine Analysen für diesen Benutzer gefunden."}), 404
    
        analyses_list = [
            {
                "image_id": analysis.image_id,
                "analysis_date": analysis.analysis_date,
                "result": analysis.result,
                "confidence_score": analysis.confidence_score,
            } for analysis in analyses
        ]

        return jsonify(analyses_list), 200
    