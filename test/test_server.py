import json,os
import logging
import sys
import config
import requests
from flask import Flask, request, Response, jsonify
from flask_restful import Api, Resource, reqparse
from flasgger import Swagger, swag_from


if __name__ == "__main__":
  # Setup Flask Server
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
  swagger = Swagger(app, template= template)
  app.config.from_object(config.Config)
  api = Api(app)


          

  import todo 

  ## Api resource routing
  api.add_resource(todo.Todo, '/stats')

  app.run(debug=True)