from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from backend import create_app, db, login_manager


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8000)