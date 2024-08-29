# vote.py

from app import db


class Vote(db.Model):
    __tablename__ = "votes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    answer_id = db.Column(db.Integer, db.ForeignKey("answers.id"))
    vote_type = db.Column(db.String(4), nullable=False)  # 'up' or 'down'

    __table_args__ = (
        db.CheckConstraint("(question_id IS NULL) != (answer_id IS NULL)"),  # XOR
    )
