# questions.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app import db
from app.models.question import Question
from app.models.tag import Tag
from app.models.vote import Vote
from app.utils.ai_helper import (
    get_ai_insights,
    get_ai_suggested_tags,
    get_ai_question_summary,
    get_ai_answer_ranking,
    get_ai_similar_questions,
)

bp = Blueprint("questions", __name__)


@bp.route("/ask", methods=["GET", "POST"])
@login_required
def ask_question():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]

        suggested_tags = get_ai_suggested_tags(title, body)

        summary = get_ai_question_summary(title, body)
        if summary is None:
            summary = "Unable to generate summary at this time."

        question = Question(
            title=title, body=body, user_id=current_user.id, summary=summary
        )

        tags = (
            request.form["tags"].split(",") if request.form["tags"] else suggested_tags
        )

        for tag_name in tags:
            tag = Tag.query.filter_by(name=tag_name.strip()).first()
            if not tag:
                tag = Tag(name=tag_name.strip())
            question.tags.append(tag)

        db.session.add(question)
        db.session.commit()

        flash("Your question has been posted!")
        return redirect(url_for("questions.question_detail", question_id=question.id))

    return render_template("ask_question.html")


@bp.route("/question/<int:question_id>/vote", methods=["POST"])
@login_required
def vote_question(question_id):
    question = Question.query.get_or_404(question_id)
    vote_type = request.form["vote_type"]

    existing_vote = Vote.query.filter_by(
        user_id=current_user.id, question_id=question_id
    ).first()

    if existing_vote:
        if existing_vote.vote_type != vote_type:
            question.votes += 2 if vote_type == "up" else -2
            existing_vote.vote_type = vote_type
        else:
            question.votes += -1 if vote_type == "up" else 1
            db.session.delete(existing_vote)
    else:
        new_vote = Vote(
            user_id=current_user.id, question_id=question_id, vote_type=vote_type
        )
        db.session.add(new_vote)
        question.votes += 1 if vote_type == "up" else -1

    db.session.commit()
    return redirect(url_for("questions.question_detail", question_id=question.id))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = Question.query.get_or_404(question_id)
    question.views += 1
    db.session.commit()

    ai_insights = get_ai_insights(question.title, question.body)
    if ai_insights is None:
        ai_insights = "Unable to generate AI insights at this time."

    if question.summary is None:
        question.summary = get_ai_question_summary(question.title, question.body)
        if question.summary is None:
            question.summary = "Unable to generate summary at this time."
        db.session.commit()

    answers_list = list(question.answers)

    ranking = get_ai_answer_ranking(question.body, answers_list)

    ranked_answers = [
        answers_list[i - 1] for i in ranking if 1 <= i <= len(answers_list)
    ]

    similar_question_ids = get_ai_similar_questions(
        question.title, question.body, Question.query.all()
    )
    similar_questions = Question.query.filter(
        Question.id.in_(similar_question_ids)
    ).all()

    return render_template(
        "question_detail.html",
        question=question,
        ai_insights=ai_insights,
        ranked_answers=ranked_answers,
        similar_questions=similar_questions,
    )
