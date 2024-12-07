from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

update_email_bp = Blueprint("update_email", __name__)

@update_email_bp.route("/update-email", methods=["PUT"])
@jwt_required()
def update_email():
    user_id = get_jwt_identity()
    new_email = request.form.get("email")
    response = UserService.update_email(user_id, new_email)

    return response
    