from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Konfiguration
    app.config.from_object('config.Config')

    # Datenbank mit Flask-App initialisieren
    db.init_app(app)
    jwt.init_app(app)
    
    # Registriere Blueprints
    from .routes.authentication.login import login_bp
    from .routes.skin_lesion_analysis.upload_skin_lesion import upload_skin_lesion_bp
    from .routes.skin_lesion_analysis.analyze_skin_lesion import analyze_skin_lesion_bp
    from .routes.skin_lesion_analysis.get_all_analyses import get_all_analyses_bp
    from .routes.account.register import register_bp
    from .routes.account.delete import delete_account_bp
    from .routes.account.update_theme import update_theme_bp
    from .routes.account.update_first_name import update_first_name_bp
    from .routes.account.update_last_name import update_last_name_bp
    from .routes.account.update_username import update_username_bp
    from .routes.account.update_email import update_email_bp
    from .routes.account.update_password import update_password_bp

    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(upload_skin_lesion_bp)
    app.register_blueprint(analyze_skin_lesion_bp)
    app.register_blueprint(get_all_analyses_bp)
    app.register_blueprint(delete_account_bp)
    app.register_blueprint(update_theme_bp)
    app.register_blueprint(update_first_name_bp)
    app.register_blueprint(update_last_name_bp)
    app.register_blueprint(update_username_bp)
    app.register_blueprint(update_email_bp)
    app.register_blueprint(update_password_bp)

    return app
