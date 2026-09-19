from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user

from models import db
from models import User
from models import Task

from forms import RegisterForm
from forms import LoginForm
from forms import TaskForm

from datetime import date

routes = Blueprint("routes", __name__)


@routes.route("/")
def home():
    return render_template("index.html")


@routes.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():

            flash("Email already registered.")

            return redirect(url_for("routes.register"))

        user = User(
            username=form.username.data,
            email=form.email.data
        )

        user.set_password(form.password.data)

        db.session.add(user)

        db.session.commit()

        flash("Registration successful.")

        return redirect(url_for("routes.login"))

    return render_template("register.html", form=form)


@routes.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and user.check_password(form.password.data):

            login_user(user)

            return redirect(url_for("routes.dashboard"))

        flash("Invalid email or password.")

    return render_template("login.html", form=form)


@routes.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = TaskForm()

    # Handle adding a new task
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            category=form.category.data,
            user_id=current_user.id
        )

        db.session.add(task)
        db.session.commit()

        flash("Task added successfully!")

        return redirect(url_for("routes.dashboard"))


    # Get search/filter values
    search = request.args.get("search", "")
    priority = request.args.get("priority", "")
    category = request.args.get("category", "")

    # Build query
    query = Task.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(Task.title.contains(search))

    if priority:
        query = query.filter_by(priority=priority)

    if category:
        query = query.filter_by(category=category)

    tasks = query.order_by(Task.due_date).all()

    # ---------------------------
    # Progress Bar Calculations
    # ---------------------------

    total_tasks = len(tasks)

    completed_tasks = len(
        [task for task in tasks if task.completed]
    )

    progress = 0

    if total_tasks > 0:
        progress = round(
            (completed_tasks / total_tasks) * 100
        )

    # Overdue tasks
    overdue_tasks = Task.query.filter(
        Task.user_id == current_user.id,
        Task.completed == False,
        Task.due_date < date.today()
    ).count()

    # ---------------------------

    return render_template(
        "dashboard.html",
        form=form,
        tasks=tasks,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        overdue_tasks=overdue_tasks,
        progress=progress,
        today=date.today()
    )

@routes.route("/task/<int:task_id>/complete")
@login_required
def complete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    task.completed = not task.completed

    db.session.commit()

    if task.completed:
        flash("Task marked as completed!", "success")
    else:
        flash("Task marked as pending.", "info")

    return redirect(url_for("routes.dashboard"))

@routes.route("/task/<int:task_id>/delete")
@login_required
def delete_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(task)

    db.session.commit()

    flash("Task deleted successfully.", "danger")

    return redirect(url_for("routes.dashboard"))

@routes.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@login_required
def edit_task(task_id):

    task = Task.query.filter_by(
        id=task_id,
        user_id=current_user.id
    ).first_or_404()

    form = TaskForm(obj=task)

    if form.validate_on_submit():

        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.category = form.category.data

        db.session.commit()

        flash("Task updated successfully.", "success")

        return redirect(url_for("routes.dashboard"))

    return render_template(
        "edit_task.html",
        form=form,
        task=task
    )


@routes.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("routes.home"))