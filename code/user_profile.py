import json,os
import logging
import sys
import config
import requests
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from


# from flask_jsonpify import jsonify

from collections import OrderedDict

from database import Database

class UserProfile(Resource):
  def __init__(self):
        self.user_id = 0
        self.user_name = ""
        self.user_last_name = "" 
        self.user_email = "" 
        self.user_mobile = ""
        self.distance = 0
        self.tags = ""

  def _create_json(self):
      # query_object = OrderedDict([("user_id",  self.user_id),
      #                     ("user_name",  self.user_name ),
      #                     ("user_mobile",  self.user_mobile),
      #                     ("distance",  self.distance),
      #                     ("tags",  self.tags )])

      query_object = dict()
      
      # query_object["user_id"] = self.user_id
      query_object["name"] = self.user_name 
      query_object["last_name"] = self.user_last_name 
      query_object["email"] = self.user_email 
      query_object["mobile"] = self.user_mobile
      query_object["distance"] = self.distance
      query_object["tags"] = self.tags 

      return query_object

  def dump(self):
      print(f"""user_id = {self.user_id},
                name = {self.user_name},
                last_name = {self.user_last_name},
                email = {self.user_email},
                mobile = {self.user_mobile},
                distance = {self.distance}, 
                tags = {self.tags}""")

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
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    db = Database()
    db.read_user_info(self, user_id)

    if lat is None or lng is None:
        resp = jsonify(self._create_json())
        resp.status_code = 200
    else:
        results = db.find_nearest_points(lat, lng, self.distance)

        resp = jsonify(results)
        resp.status_code = 200

    return resp
    
    # return jsonify({
    #           "sum": numsum,
    #           "product": prod,
    #           "division": div
    #       })

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