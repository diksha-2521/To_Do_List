from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    PasswordField,
    DateField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length
)


class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3)]
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )

    confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password")
        ]
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

    submit = SubmitField("Login")



class TaskForm(FlaskForm):

    title = StringField(
        "Task",
        validators=[DataRequired()]
    )

    description = TextAreaField("Description")

    due_date = DateField(
        "Due Date",
        format="%Y-%m-%d"
    )

    priority = SelectField(
        "Priority",
        choices=[
            ("High","High"),
            ("Medium","Medium"),
            ("Low","Low")
        ]
    )

    category = SelectField(
        "Category",
        choices=[
            ("Work","Work"),
            ("Study","Study"),
            ("Personal","Personal"),
            ("Shopping","Shopping")
        ]
    )

    submit = SubmitField("Add Task")