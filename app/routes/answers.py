# answers.py

from flask import Blueprint, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.question import Question
from app.models.answer import Answer
from app.models.vote import Vote
from app.utils.ai_helper import get_ai_answer_review

bp = Blueprint("answers", __name__)


@bp.route("/question/<int:question_id>/answer", methods=["POST"])
@login_required
def post_answer(question_id):
    question = Question.query.get_or_404(question_id)
    answer_body = request.form["answer_body"]

    answer = Answer(body=answer_body, author=current_user, question=question)
    db.session.add(answer)
    db.session.commit()

    ai_review = get_ai_answer_review(question.body, answer_body)
    flash(f"Your answer has been posted! AI Review: {ai_review}")

    return redirect(url_for("questions.question_detail", question_id=question_id))


@bp.route("/answer/<int:answer_id>/vote", methods=["POST"])
@login_required
def vote_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    vote_type = request.form["vote_type"]

    existing_vote = Vote.query.filter_by(
        user_id=current_user.id, answer_id=answer_id
    ).first()

    if existing_vote:
        if existing_vote.vote_type != vote_type:
            answer.votes += 2 if vote_type == "up" else -2
            existing_vote.vote_type = vote_type
        else:
            answer.votes += -1 if vote_type == "up" else 1
            db.session.delete(existing_vote)
    else:
        new_vote = Vote(
            user_id=current_user.id, answer_id=answer_id, vote_type=vote_type
        )
        db.session.add(new_vote)
        answer.votes += 1 if vote_type == "up" else -1

    db.session.commit()
    return redirect(
        url_for("questions.question_detail", question_id=answer.question_id)
    )


@bp.route("/answer/<int:answer_id>/accept", methods=["POST"])
@login_required
def accept_answer(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question = answer.question

    if current_user != question.author:
        flash("You can only accept answers to your own questions.")
        return redirect(url_for("questions.question_detail", question_id=question.id))

    for a in question.answers:
        a.is_accepted = False

    answer.is_accepted = True
    db.session.commit()

    flash("Answer has been accepted.")
    return redirect(url_for("questions.question_detail", question_id=question.id))
