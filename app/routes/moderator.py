# moderator.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.question import Question
from app.models.answer import Answer
from app.utils.decorators import moderator_required

bp = Blueprint("moderator", __name__, url_prefix="/moderator")


@bp.route("/moderate")
@login_required
@moderator_required
def moderate():
    reported_questions = Question.query.filter(Question.reported == True).all()
    return render_template(
        "moderate.html",
        reported_questions=reported_questions,
    )


@bp.route("/approve_question/<int:question_id>", methods=["POST"])
@moderator_required
def approve_question(question_id):
    question = Question.query.get_or_404(question_id)
    question.reported = False
    question.reported_by = None
    try:
        db.session.commit()
        flash("Question approved successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while approving the question.", "error")
    return redirect(url_for("moderator.moderate"))


@bp.route("/delete_question/<int:question_id>", methods=["POST"])
@moderator_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    try:
        db.session.delete(question)
        db.session.commit()
        flash("Question deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the question.", "error")
    return redirect(url_for("moderator.moderate"))
