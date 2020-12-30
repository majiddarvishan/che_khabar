"""Initialize Flask app."""
from flask import Flask
# from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    # app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)

    with app.app_context():
        from . import advertisement_profile
        from . import user_profile

        db.create_all()

    from . import my_json_encoder
    app.json_encoder = my_json_encoder.MyJSONEncoder

    return app
