#!/usr/bin/python3

# https://www.tutorialspoint.com/python3/python_database_access.htm
# https://flask.palletsprojects.com/en/0.12.x/config/#config
# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
# https://medium.com/the-era-of-apis/how-to-build-an-api-in-python-with-flask-rapidapi-a336af4632cd

from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

import my_json_encoder

import user_profile
import advertisement
import database

if __name__ == "__main__":
    app = Flask(__name__)
    app.json_encoder = my_json_encoder.MyJSONEncoder
    app.config['JSON_SORT_KEYS'] = False
    api = Api(app)

    # api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")
    api.add_resource(user_profile.UserProfile, '/users', endpoint='/users')
    api.add_resource(user_profile.UserProfile, '/users/<user_id>', endpoint='/users/<user_id>')

    api.add_resource(advertisement.Advertisement, '/advertises')

    # 35.6997223, 51.3380470
    # 35.699724, 51.338048
    # database.find_nearest_points(35.699720, 51.337974, 100)

    app.run(host='172.23.10.20', port='5002')