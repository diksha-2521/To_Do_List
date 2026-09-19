import os

class Config:

    SECRET_KEY = os.environ.get("YOUR_SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///todo.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False