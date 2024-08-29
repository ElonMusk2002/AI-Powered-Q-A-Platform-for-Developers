# admin.py

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.user import User
from app.models.tag import Tag
from app.models.question import Question

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]
        user.role = request.form["role"]

        try:
            db.session.commit()
            flash("User details updated successfully!", "success")
            return redirect(url_for("admin.admin_dashboard"))
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating the user.", "error")

    return render_template("edit_user.html", user=user)


@bp.route("/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the user.", "error")

    return redirect(url_for("main.admin_dashboard"))


@bp.route("/delete_question/<int:question_id>", methods=["POST"])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)

    try:
        db.session.delete(question)
        db.session.commit()
        flash("Question deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the question.", "error")

    return redirect(url_for("main.admin_dashboard"))


@bp.route("/delete_tag/<int:tag_id>", methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    try:
        db.session.delete(tag)
        db.session.commit()
        flash("Tag deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the tag.", "error")

    return redirect(url_for("auth.admin_dashboard"))
