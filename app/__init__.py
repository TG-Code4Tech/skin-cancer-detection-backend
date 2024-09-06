from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Konfiguration
    app.config.from_object('config.Config')
    
    # Registriere Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.image_routes import image_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(image_bp)

    return app
