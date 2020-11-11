import json,os
import logging
import sys
import config
# import requests
from flask import make_response, redirect, render_template, request, url_for
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from

# from flask_jsonpify import jsonify

from collections import OrderedDict


from .models import User, db

class UserProfile(Resource):
  def __init__(self):
        self.user_id = 0
        self.user_name = ""
        self.user_last_name = "" 
        self.user_email = "" 
        self.user_mobile = ""
        self.distance = 0
        self.tags = ""

  def get(self, user_id):
    """
    post endpoint
    ---      
    tags:
      - Flast Restful APIs
    parameters:
      - name: lat
        in: query
        type: float
        required: false
        description: current latitude of user
      - name: lng
        in: query
        type: float
        required: false
        description: current longitute of user
    responses:
      500:
        description: Error The number is not float!
      200:
        description: Number statistics
        schema:
          id: stats
          properties:
            sum:
              type: integer
              description: The sum of number
            product:
              type: integer
              description: The sum of number
            division:
              type: integer
              description: The sum of number              
    """
    email = request.args.get("email")
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    if email:
        existing_user = User.query.filter(
            User.email == email
        ).first()
        if existing_user:
          if lat is None or lng is None:
            resp = jsonify(existing_user.create_json())
            resp.status_code = 200
          else:
            sql = f"""
                SELECT
                    body,
                    latitude,
                    longitude,
                    tags,
                    Convert((6371 *
                    acos(
                        cos (radians({lat})) * cos(radians(latitude)) * cos(radians(longitude) - radians({lng})) +
                        sin (radians({lat})) * sin(radians(latitude))
                        )
                    * 100
                    ), UNSIGNED ) AS distance
                FROM advertisements
                HAVING distance < {existing_user.distance} AND latitude != {lat} AND longitude != {lng}
                ORDER BY distance
                LIMIT 0 , 20;
                """
            result = db.session.execute(sql)
            # places = [row for row in result]
            # print(places)
            # print(type(places))
            # print(type(places[0]))

            from collections import namedtuple

            Record = namedtuple('Record', result.keys())
            records = [Record(*r)._asdict() for r in result.fetchall()]

            resp = jsonify(records)
            resp.status_code = 200
    else:
      resp = jsonify("please input email")
      resp.status_code = 400

    return resp  

  def post(self): 
    result = {"message": "ok"}

    try:
        for k, v in request.json.items():
            if(k == "name"):
                self.user_name = v
            elif(k == "last_name"):
                self.user_last_name = v
            elif(k == "email"):
                self.user_email = v
            elif(k == "mobile"):
                self.user_mobile = v
            elif(k == "distance"):
                self.distance = v
            elif(k == "tags"):
                self.tags = v
            else:
                print(f"{k}, {v}")
        db = Database()
        res, text = db.save_user_data(self)
        result = {"message": str(text)}

    except Exception as e:
        print(e)
        result = {"message": str(e)}

    return jsonify(result)