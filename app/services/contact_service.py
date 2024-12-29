import os
import smtplib
from app.services.user_service import UserService
from flask import jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

class ContactService:

    @staticmethod
    def send_confirmation_email(first_name, last_name, email, matter):
        if not first_name or not last_name or not email or not matter:
            return jsonify({"error": "Es konnte aufgrund von unvollständigen Angaben keine E-Mail gesendet werden."}), 404
        
        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = email
        smtp_server = "mail.gmx.net"
        smtp_port = 587
        subject = "Ihre Anfrage an Skin Cancer Detection"
        body = (f"Hallo {first_name} {last_name},\n\n"
                f"Vielen Dank für Ihre Nachricht!\n\n"
                f"Wir werden uns schnellstmöglich um Ihr Anliegen kümmern.\n\n"
                f"Freundliche Grüße\n\n"
                f"Ihr Skin Cancer Detection Team")

        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())

            return jsonify({"message": "Vielen Dank für Ihre Nachricht. Ihr Anliegen wird schnellstmöglich bearbeitet."}), 200
        except Exception as e:
            print(f"Allgemeiner Fehler beim Senden der E-Mail: {str(e)}")
            return jsonify({"error": f"Ihr Anliegen konnte leider nicht erfolgreich weitergeleitet werden. Bitte versuchen Sie es erneut."}), 500
        finally:
            server.quit()


    @staticmethod
    def redirect_matter_to_service(first_name, last_name, email, matter):
        is_first_name_valid = UserService.validate_input(first_name)
        is_last_name_valid = UserService.validate_input(last_name)
        is_email_valid, email_validation_message = UserService.validate_email(email)
        is_matter_valid = UserService.validate_input(matter)

        if not is_first_name_valid:
            return jsonify({
                "check": "backend_first_name",
                "error": "Bitte einen Vornamen angeben."
            }), 400
        
        if not is_last_name_valid:
            return jsonify({
                "check": "backend_last_name",
                "error": "Bitte einen Nachnamen angeben."
            }), 400

        if not is_email_valid:
            return jsonify({
                "check": "backend_email",
                "error": email_validation_message
            }), 400
        
        if not is_matter_valid:
            return jsonify({
                "check": "backend_matter",
                "error": "Bitte ein Anliegen angeben."
            }), 400
        
        sender = os.getenv("EMAIL_ADDRESS")
        password = os.getenv("EMAIL_PASSWORD")
        receiver = os.getenv("EMAIL_ADDRESS")
        smtp_server = "mail.gmx.net"
        smtp_port = 587
        subject = "Anfrage an Skin Cancer Detection"
        body = (
            f"Hallo Skin Cancer Detection Team,\n\n"
            f"Sender: {first_name} {last_name}\n\n"
            f"E-Mail: {email}\n\n"
            f"Anliegen:\n\n{matter}"
        )
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = receiver
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, receiver, message.as_string())
        except Exception as e:
            print(f"Allgemeiner Fehler beim Senden der E-Mail: {str(e)}")
        finally:
            server.quit()
            