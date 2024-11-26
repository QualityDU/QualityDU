from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class DevConfig(Config):
    FLASK_ENV = "development"
    TESTING = True
    DEBUG = True
    
class ProdConfig(Config):
    FLAKS_ENV = "production"
    TESTING = False
    DEBUG = False
    
class TestConfig(Config):
    FLASK_ENV = "testing"
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URL")
