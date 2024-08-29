# question.py

from app import db
from datetime import datetime

question_tags = db.Table(
    "question_tags",
    db.Column(
        "question_id", db.Integer, db.ForeignKey("questions.id"), primary_key=True
    ),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    answers = db.relationship("Answer", backref="question", lazy="dynamic")
    tags = db.relationship(
        "Tag", secondary=question_tags, backref=db.backref("questions", lazy="dynamic")
    )
    views = db.Column(db.Integer, default=0)
    votes = db.Column(db.Integer, default=0)
    reported = db.Column(db.Boolean, default=False)
    summary = db.Column(db.Text)

    user = db.relationship("User", foreign_keys=[user_id], back_populates="questions")
    reported_by_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    reported_by_user = db.relationship(
        "User", foreign_keys=[reported_by_id], back_populates="reported_questions"
    )
