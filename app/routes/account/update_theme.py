from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

update_theme_bp = Blueprint("update_theme", __name__)

@update_theme_bp.route("/update-theme", methods=["PUT"])
@jwt_required()
def update_theme():
    user_id = get_jwt_identity()
    new_theme = request.form.get("theme")
    response = UserService.update_theme(user_id, new_theme)

    return response
