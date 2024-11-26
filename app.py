from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from backend import create_app, socketio


if __name__ == "__main__":
    app = create_app()
    socketio.run(app, debug=True)
