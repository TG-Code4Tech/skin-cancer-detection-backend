from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

update_last_name_bp = Blueprint("update_last_name", __name__)

@update_last_name_bp.route("/update-last-name", methods=["PUT"])
@jwt_required()
def update_last_name():
    user_id = get_jwt_identity()
    new_last_name = request.form.get("last_name")
    response = UserService.update_last_name(user_id, new_last_name)

    return response
