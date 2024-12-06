from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

update_username_bp = Blueprint("update_username", __name__)

@update_username_bp.route("/update-username", methods=["PUT"])
@jwt_required()
def update_username():
    user_id = get_jwt_identity()
    new_username = request.form.get("username")
    response = UserService.update_username(user_id, new_username)

    return response
    