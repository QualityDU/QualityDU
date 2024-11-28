from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from backend.models import db
from flask_migrate import Migrate
from flask_socketio import SocketIO
from backend.config import DevConfig, ProdConfig, TestConfig
from dotenv import load_dotenv
from flask_cors import CORS
import os

login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)

    flask_env = os.getenv("FLASK_ENV", "development").lower()
    if flask_env == "production":
        app.config.from_object(ProdConfig)
    elif flask_env == "testing":
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    CORS(app, resources={r"*": {"origins": "*"}})

    from backend.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # with app.app_context():
    #     db.create_all()
        
    from backend.apps.core.views import core_bp
    from backend.apps.auth.views import auth_bp
    from backend.apps.chat.views import chat_bp
    from backend.apps.act.views import act_bp

    app.register_blueprint(core_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chat_bp, url_prefix="/chat")
    app.register_blueprint(act_bp, url_prefix="/act")

    login_manager.login_view = "auth_bp.login"
    socketio.init_app(app, cors_allowed_origins="*")

    return app