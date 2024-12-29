from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

update_password_bp = Blueprint("update_password", __name__)

@update_password_bp.route("/update-password", methods=["PUT"])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    current_password = request.form.get("current_password")
    new_password = request.form.get("password")
    new_password_confirmation = request.form.get("password_confirmation")
    response = UserService.update_password(user_id, current_password, new_password, new_password_confirmation)

    return response
