from app import db

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_image = db.Column(db.String(50), nullable=True)
    theme = db.Column(db.Enum("light", "dark", name="theme_enum"), nullable=False, default="light")

    def __repr__(self):
        return f"<User {self.user_id} - {self.username} - Email: {self.email} - First_name: {self.first_name} - Last_name: {self.last_name}>"
