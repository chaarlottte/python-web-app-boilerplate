from ..models import db
import flask_login, json

class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return json.dumps({
            "id": self.id,
            "username": self.username,
            "password": self.password
        })
    pass