# auth.py

import os
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app import db
from app.models.question import Question
from app.models.tag import Tag
from app.utils.decorators import admin_required, moderator_required

bp = Blueprint("auth", __name__)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login_type = request.form["login_type"]
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)

            if login_type == "admin":
                if user.is_admin:
                    return redirect(url_for("auth.admin_dashboard"))
                else:
                    flash("You do not have admin access.")
            elif login_type == "moderator":
                if user.is_moderator:
                    return redirect(url_for("auth.moderate"))
                else:
                    flash("You do not have moderator access.")
            else:
                return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/dashboard")
@login_required
@admin_required
def admin_dashboard():
    users = User.query.all()
    questions = Question.query.all()
    tags = Tag.query.all()
    return render_template(
        "admin_dashboard.html", users=users, questions=questions, tags=tags
    )


@bp.route("/moderate")
@login_required
@moderator_required
def moderate():
    reported_questions = Question.query.filter(Question.reported == True).all()
    return render_template(
        "moderate.html",
        reported_questions=reported_questions,
    )


@bp.route("/report_question/<int:question_id>", methods=["POST"])
@login_required
def report_question(question_id):
    question = Question.query.get_or_404(question_id)
    if not question.reported:
        question.reported = True
        question.reported_by_id = current_user.id
        try:
            db.session.commit()
            flash("The question has been reported to the moderators.", "success")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while reporting the question.", "error")
    else:
        flash("This question has already been reported.", "warning")

    return redirect(url_for("main.index"))
