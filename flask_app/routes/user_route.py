from flask import request, jsonify
from flasgger import Swagger, swag_from
from datetime import datetime
from collections import OrderedDict
from flask import current_app as app

from flask_app import db
from flask_app.models import users_model, tags_model, user_tags_model

@app.route("/users/<user_email>", methods=["GET"])
def get_user_info(user_email : str):
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
def add_new_user():
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