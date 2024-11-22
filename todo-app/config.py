# Placeholder for Python file
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:12345@localhost:5432/todo_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
