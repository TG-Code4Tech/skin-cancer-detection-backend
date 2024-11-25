from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Konfiguration
    app.config.from_object('config.Config')

    # Datenbank mit Flask-App initialisieren
    db.init_app(app)
    
    # Registriere Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.upload_skin_lesion import upload_skin_lesion_bp
    from .routes.analyze_skin_lesion import analyze_skin_lesion_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_skin_lesion_bp)
    app.register_blueprint(analyze_skin_lesion_bp)

    return app
