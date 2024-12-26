from flask import Blueprint, request
from app.services.user_service import UserService
from app.services.contact_service import ContactService

contact_bp= Blueprint("contact", __name__)

@contact_bp.route("/contact-us", methods=["POST"])
def send_confirmation_email():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    matter = request.form.get("matter")
    
    ContactService.redirect_matter_to_service(first_name, last_name, email, matter)
    response = ContactService.send_confirmation_email(first_name, last_name, email, matter)

    return response
    