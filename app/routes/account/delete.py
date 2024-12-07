from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

delete_account_bp = Blueprint("delete_account", __name__)

@delete_account_bp.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    response = UserService.delete_user(user_id)

    return response
    