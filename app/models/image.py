from app import db
from app.models.user import User

class Image(db.Model):
    __tablename__ = "images"

    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    image = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", backref="images")

    def __repr__(self):
        return f"<Image {self.image_id} - {self.image}>"
