from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import UserService

get_user_data_bp = Blueprint("get_user_data", __name__)

@get_user_data_bp.route("/get-user-data", methods=["GET"])
@jwt_required()
def get_user_data():
    user_id = get_jwt_identity()
    response = UserService.get_user_data(user_id)

    return response
    