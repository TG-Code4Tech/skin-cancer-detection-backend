from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    # Weitere Felder für die Bildverarbeitung

    def __repr__(self):
        return f'<Image {self.filename}>'
