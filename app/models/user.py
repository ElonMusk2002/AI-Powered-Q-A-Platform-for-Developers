# user.py

from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    reputation = db.Column(db.Integer, default=0)
    questions = db.relationship(
        "Question",
        foreign_keys="Question.user_id",
        back_populates="user",
        lazy="dynamic",
    )
    reported_questions = db.relationship(
        "Question",
        foreign_keys="Question.reported_by_id",
        back_populates="reported_by_user",
        lazy="dynamic",
    )
    answers = db.relationship("Answer", backref="author", lazy="dynamic")
    is_admin = db.Column(db.Boolean, default=False)
    is_moderator = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
