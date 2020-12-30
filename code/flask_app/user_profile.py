import json,os
import logging
import sys
import config
# import requests
from flask import make_response, redirect, render_template, request, url_for
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from
from datetime import datetime

# from flask_jsonpify import jsonify

from collections import OrderedDict

from .models import user, advertisement
from flask_app import db

class UserProfile(Resource):
  def get(self, user_email : str):
    """
    get endpoint
    ---      
    tags:
      - user
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email of user
    responses:
      400:
        description: missing some parameters
      200:
        description: return user's information
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
    if user_email:
        existing_user = user.User.query.filter(
            user.User.email == user_email
        ).first()
        if existing_user:
            resp = jsonify(existing_user.create_json())
            resp.status_code = 200
        else:
          resp = jsonify("user with this email is not available")
          resp.status_code = 400
    else:
      resp = jsonify("please input email")
      resp.status_code = 400

    return resp  

  def post(self): 
    for k, v in request.json.items():
        if(k == "first_name"):
            first_name = v
        elif(k == "last_name"):
            last_name = v
        elif(k == "email"):
            email = v
        elif(k == "mobile"):
            mobile = v
        elif(k == "distance"):
            distance = v
        elif(k == "tags"):
            tags = v
        else:
            print(f"{k}, {v}")

    if email:
      existing_user = user.User.query.filter(
          user.User.email == email
      ).first()
      if existing_user:
        result = jsonify("User with this email is already exist") 
        result.status_code = 400
        return result
      else:
        new_user = user.User(firstname=first_name,
                        lastname=last_name,
                        email=email,
                        mobile=mobile,
                        created=datetime.now(),
                        distance=distance,
                        bio="In West Philadelphia born and raised, \
                        on the playground is where I spent most of my days",
                        tags=tags
                        )
        db.session.add(new_user) 
        db.session.commit()  
        
        return jsonify("user profile successfully created!") 
    else:
      return jsonify("missing some parameters!") 

    return jsonify("missing some parameters!") 
    # return make_response(f"missing some parameters!")