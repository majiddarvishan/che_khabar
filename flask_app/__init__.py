# https://hackersandslackers.com/flask-sqlalchemy-database-models/

"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("flask_app.config.Config")
    # app.config['JSON_SORT_KEYS'] = False
    
    if not app.config['GOOGLE_CLIENT_ID'] or not app.config['GOOGLE_CLIENT_SECRET']:
        raise RuntimeError('Environment not set up, see "Running":\n' + __doc__)
    
    # User session management setup
    # https://flask-login.readthedocs.io/en/latest
    login_manager.init_app(app)

    db.init_app(app)

    with app.app_context():
        from .routes import advertisement_route
        from .routes import user_route
        
        from .models import advertisement_tags_model
        from .models import advertisements_model
        from .models import user_tags_model
        from .models import users_model
        from .models import tags_model

        db.create_all()
        
    # OAuth 2 client setup
    oauth_client = WebApplicationClient(app.config['GOOGLE_CLIENT_ID'])

    from . import my_json_encoder
    app.json_encoder = my_json_encoder.MyJSONEncoder
    
    # Create an APISpec
    template = {
    "swagger": "2.0",
    "info": {
        "title": "Che khabar",
        "description": "This is Swagger of Che Khabar Restful API's description",
        "version": "0.0.1",
        "contact": {
        "name": "Majid Darvishan",
        "url": "https://majiddarvishan.org",
        }
    },
    "securityDefinitions": {
        "Bearer": {
        "type": "apiKey",
        "name": "Authorization",
        "in": "header",
        "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [
        {
        "Bearer": [ ]
        }
    ]

    }

    app.config['SWAGGER'] = {
        'title': 'Che Khabar API',
        'uiversion': 3,
        "specs_route": "/swagger/"
    }

    swagger = Swagger(app, template= template)


    return app
