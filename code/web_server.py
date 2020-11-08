#!python

# https://www.tutorialspoint.com/python3/python_database_access.htm
# https://flask.palletsprojects.com/en/0.12.x/config/#config
# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
# https://medium.com/the-era-of-apis/how-to-build-an-api-in-python-with-flask-rapidapi-a336af4632cd
# https://kanoki.org/2020/07/18/python-api-documentation-using-flask-swagger/

from flask import Flask, request
from flask_restful import Resource, Api
# import config
from json import dumps
from flask_jsonpify import jsonify
from flasgger import Swagger, swag_from

import json,os
import logging
import sys
import config
import requests
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse

import my_json_encoder

import user_profile
import advertisement
import database

if __name__ == "__main__":
    app = Flask(__name__)

    # Create an APISpec
    template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Restful Swagger Demo",
        "description": "A Demof for the Flask-Restful Swagger Demo",
        "version": "0.1.1",
        "contact": {
        "name": "Kanoki",
        "url": "https://Kanoki.org",
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
        'title': 'My API',
        'uiversion': 3,
        "specs_route": "/swagger/"
    }

    app.json_encoder = my_json_encoder.MyJSONEncoder

    swagger = Swagger(app, template= template)
    app.config.from_object(config.Config)

    # app.config['JSON_SORT_KEYS'] = False
    api = Api(app)

    # api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")

    # api.add_resource(user_profile.UserProfile, '/users', endpoint='/users')
    api.add_resource(user_profile.UserProfile, '/users/<user_id>', endpoint='/users/<user_id>')

    api.add_resource(advertisement.Advertisement, '/advertises')
    api.add_resource(advertisement.Advertisement, '/advertises/<advertise_id>', endpoint='/advertises/<advertise_id>')

    # 35.6997223, 51.3380470
    # 35.699724, 51.338048
    # database.find_nearest_points(35.699720, 51.337974, 100)

    app.run(debug=True, host='127.0.0.1', port='5000')
