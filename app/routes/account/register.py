from flask import Blueprint, request
from app.services.user_service import UserService

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    password_confirmation = request.form.get("password_confirmation")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    response = UserService.register_user(username, email, password, password_confirmation, first_name, last_name)

    return response
    