from app import db
from datetime import datetime, timezone
from app.models.user import User
from app.models.image import Image

class Analysis(db.Model):
    __tablename__ = "analyses"

    analysis_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    analysis_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    result = db.Column(db.String(255), nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey("images.image_id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", backref="analyses")
    image = db.relationship("Image", backref="analyses")

    def __repr__(self):
        return f"<Analysis {self.analysis_id} - {self.result} - Confidence: {self.confidence_score}>"
