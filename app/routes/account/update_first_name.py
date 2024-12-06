from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

update_first_name_bp = Blueprint("update_first_name", __name__)

@update_first_name_bp.route("/update-first-name", methods=["PUT"])
@jwt_required()
def update_first_name():
    user_id = get_jwt_identity()
    new_first_name = request.form.get("first_name")
    response = UserService.update_first_name(user_id, new_first_name)

    return response
