# main.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models.question import Question
from app.models.user import User
from app.models.tag import Tag
from app.models.answer import Answer
from app.utils.ai_helper import get_ai_suggested_tags
from app.utils.decorators import admin_required, moderator_required

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    questions = Question.query.order_by(Question.timestamp.desc()).paginate(
        page=page, per_page=10
    )
    return render_template("index.html", questions=questions)


@bp.route("/search")
def search():
    query = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    questions = (
        Question.query.filter(
            or_(Question.title.ilike(f"%{query}%"), Question.body.ilike(f"%{query}%"))
        )
        .order_by(Question.timestamp.desc())
        .paginate(page=page, per_page=10)
    )
    return render_template("search_results.html", questions=questions, query=query)


@bp.route("/user/<username>")
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    questions = user.questions.order_by(Question.timestamp.desc()).paginate(
        page=page, per_page=5
    )
    answers = user.answers.order_by(Answer.timestamp.desc()).paginate(
        page=page, per_page=5
    )
    return render_template(
        "user_profile.html", user=user, questions=questions, answers=answers
    )


@bp.route("/tags")
def tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("tags.html", tags=tags)


@bp.route("/tag/<tag_name>")
def tag_questions(tag_name):
    tag = Tag.query.filter_by(name=tag_name).first_or_404()
    page = request.args.get("page", 1, type=int)
    questions = tag.questions.order_by(Question.timestamp.desc()).paginate(
        page=page, per_page=10
    )
    return render_template("tag_questions.html", tag=tag, questions=questions)


@bp.route("/api/suggest_tags", methods=["POST"])
def suggest_tags():
    data = request.json
    title = data.get("title", "")
    body = data.get("body", "")
    suggested_tags = get_ai_suggested_tags(title, body)
    return jsonify({"tags": suggested_tags})
