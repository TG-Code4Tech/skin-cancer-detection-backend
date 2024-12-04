from app import db
from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User

delete_account_bp = Blueprint("delete_account", __name__)

@delete_account_bp.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "Es konnte kein Benutzer gefunden werden."}), 404
    
    db.session.delete(user)
    db.session.commit()

    response = make_response(jsonify({
        "message": "Account erfolgreich gelöscht.",
    }), 200)

    response.delete_cookie("jwt_access_token")

    return response
    