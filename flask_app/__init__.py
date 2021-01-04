# https://hackersandslackers.com/flask-sqlalchemy-database-models/

"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("flask_app.config.Config")
    # app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)

    with app.app_context():
        from .routes import advertisement_routes
        from .routes import user_routes
        
        from .models import advertisement_tags
        from .models import advertisements
        from .models import user_tags
        from .models import users
        from .models import tags

        db.create_all()

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
