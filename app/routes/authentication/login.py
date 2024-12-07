from flask import Blueprint, request
from app.services.authentication_service import AuthenticationService

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    username_or_email = request.form.get("username_or_email")
    password = request.form.get("password")
    response = AuthenticationService.login_user(username_or_email, password)

    return response
    