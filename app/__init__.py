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
    from .routes.image_routes import image_bp
    from .routes.analyze_skin_lesion import analyze_skin_lesion_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(analyze_skin_lesion_bp)

    return app
