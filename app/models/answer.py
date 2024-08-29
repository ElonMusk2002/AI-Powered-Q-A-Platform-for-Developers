# answer.py

from app import db
from datetime import datetime


class Answer(db.Model):
    __tablename__ = "answers"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    votes = db.Column(db.Integer, default=0)
    is_accepted = db.Column(db.Boolean, default=False)
    reported = db.Column(db.Boolean, default=False)
