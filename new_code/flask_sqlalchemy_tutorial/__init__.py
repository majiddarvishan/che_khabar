"""Initialize Flask app."""
from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)

    # Create database tables for our data models
    with app.app_context():
        db.create_all() 

    # app.config['JSON_SORT_KEYS'] = False
    api = Api(app)

    # api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")

    from . import user_profile
    api.add_resource(user_profile.UserProfile, '/users', endpoint='/users')
    api.add_resource(user_profile.UserProfile, '/users/<user_id>', endpoint='/users/<user_id>')

    # api.add_resource(advertisement.Advertisement, '/advertises')
    # api.add_resource(advertisement.Advertisement, '/advertises/<advertise_id>', endpoint='/advertises/<advertise_id>')

    # db.create_all()  # Create database tables for our data models

    from . import my_json_encoder
    app.json_encoder = my_json_encoder.MyJSONEncoder

    return app
