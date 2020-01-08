#!/usr/bin/python3

# https://www.tutorialspoint.com/python3/python_database_access.htm

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

    api.add_resource(user_profile.UserProfile, '/users')
    # api.add_resource(user_profile.UserProfile, '/users/<user_id>') 

    api.add_resource(advertisement.Advertisement, '/advertises')

    # 35.6997223, 51.3380470
    # 35.699724, 51.338048
    database.find_nearest_points(35.699720, 51.337974, 100)

    # app.run(host='172.23.10.20', port='5002')