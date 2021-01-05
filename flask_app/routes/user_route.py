from flask import request, jsonify
from flasgger import Swagger, swag_from
from datetime import datetime
from collections import OrderedDict
from flask import current_app as app

from flask_app import db
from flask_app.models import users_model, tags_model, user_tags_model
from flask_expects_json import expects_json

post_user_schema = {
  "type": "object",
  "properties": {
    "email": {
      "type": "string",
      "pattern": "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    },
    "first_name": {
      "type": "string"
    },
    "last_name": {
      "type": "string"
    },
    "mobile": {
      "type": "string",
      "pattern": "^(09)(\d{9})$"
    },
    "distance": {
      "type": "integer"
    },
    "tags": {
      "type": "string"
    }
  },
  "required": [
    "email",
    "first_name",
    "last_name",
    "mobile"
  ]
}


@app.route("/users/<user_email>", methods=["GET"])
def get_user_info(user_email : str):
  """
  get user information
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
        id: get_user_info
        properties:
          first_name:
            type: string
            description: The first name of user
          last_name:
            type: string
            description: The last name of user
          email:
            type: string
            description: The email of user
          mobile:
            type: string
            description: The mobile number of user
          distance:
            type: integer
            description: The expected distance of user
  """
  
  if user_email:
      existing_user = users_model.User.query.filter(
          users_model.User.email == user_email
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

@app.route("/users", methods=["POST"])
@expects_json(post_user_schema)
def add_new_user():
  """
  add new user
  ---
  tags:
    - user
  parameters:
    - name: first_name
      in: body
      type: string
      required: true
      description: first name of user
    - name: last_name
      in: body
      type: string
      required: true
      description: last name of user
    - name: email
      in: body
      type: string
      required: true
      description: email of user
    - name: mobile
      in: body
      type: string
      required: true
      description: mobile number of user
    - name: distance
      in: body
      type: integer
      required: false
      description: expected radius
    - name: tags
      in: body
      type: string
      required: false
      description: favorite tags
  responses:
    400:
      description: missing some parameters
    200:
      description: successfully add new user
  """
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
          recieved_tags = v
      else:
          print(f"{k}, {v}")

  if email:
    existing_user = users_model.User.query.filter(
        users_model.User.email == email
    ).first()
    if existing_user:
      result = jsonify("User with this email is already exist")
      result.status_code = 400
      return result
    else:
      new_user = users_model.User(firstname=first_name,
                      lastname=last_name,
                      email=email,
                      mobile=mobile,
                      created=datetime.now(),
                      distance=distance,
                      bio="In West Philadelphia born and raised, \
                      on the playground is where I spent most of my days"
                      )
      db.session.add(new_user)
      db.session.commit()

      tag_list = recieved_tags.split(",")
      for tn in tag_list:
        t = tags_model.Tag.query.filter(
            tags_model.Tag.name == tn
        ).first()
        if(t):
          tag_id = t.tag_id
        else:
          new_tag = tags_model.Tag(name=tn)
          db.session.add(new_tag)
          db.session.commit()
          tag_id = new_tag.tag_id

        new_user_tag = user_tags_model.UsertTag(user_id=new_user.id, tag_id=tag_id)
        db.session.add(new_user_tag)
        db.session.commit()

      return jsonify("user profile successfully created!")
  else:
    return jsonify("missing some parameters!")
    # return make_response(f"missing some parameters!")