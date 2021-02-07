"""Flask configuration variables."""
from os import environ, path, urandom
from dotenv import load_dotenv

class Config:
    """Set Flask configuration from .env file."""
    
    basedir = path.abspath(path.dirname(__file__))
    load_dotenv(path.join(basedir, ".env"))

    # General Config
    SECRET_KEY = environ.get("SECRET_KEY")  or urandom(24)
    FLASK_APP = environ.get("FLASK_APP")
    FLASK_ENV = environ.get("FLASK_ENV")

    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
