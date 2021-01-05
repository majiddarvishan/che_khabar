from flask_jsonpify import jsonify
from flask import request
from flask import current_app as app

from flask_app import db
from flask_app.models import users_model, advertisements_model, tags_model, advertisement_tags_model

@app.route("/advertisements/<user_email>", methods=["GET"])
def get_all_advetisements(user_email: str):
  """
  get all advertisements of user
  ---
  tags:
  - advertisement
  parameters:
  - name: email
    in: path
    type: string
    required: true
    description: email of user
  responses:
    400:
      description: this user is not available
    200:
      description: get all advertisements of user
      schema:
        id: get_all_user_advetisements
        properties:
          description:
            type: string
            description: The description of advertisement
          latitude:
            type: number
            format: float
            description: The latitude of advertisement
          longitude:
            type: number
            format: float
            description: The longitude of advertisement
          start_time:
            type: string
            format: date-time
            description: The start time of advertisement
          end_time:
            type: string
            format: date-time
            description: The end time of advertisement
    """

  usr = users_model.User.query.filter(
      users_model.User.email == user_email
  ).first()

  if(usr):
      advs = advertisements_model.Advertisement.query.filter(
          advertisements_model.Advertisement.user_id == usr.id
      ).all()

      l = list()
      for adv in advs:
          l.append(adv.create_json())

      result = jsonify(l)

  else:
      result = jsonify("User with this email is not available")
      result.status_code = 400

  return result

@app.route("/advertisements", methods=["GET"])
def get_Advertisements_by_location():
  """
  get advertisements according to user location
  ---
  tags:
  - advertisement
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
  - name: distance
    in: query
    type: integer
    required: false
    description: user prefered distance
  responses:
    400:
      description: missing some parameters
    200:
      description: if latitude and longitude don't available, return user's information. otherwise return places according to user's location
      schema:
        id: get_adv_by_loc
        properties:
          description:
            type: string
            description: The description of advertisement
          distance:
            type: integer
            description: The distance between advertisement and user's current location
          latitude:
            type: number
            format: float
            description: The latitude of advertisement
          longitude:
            type: number
            format: float
            description: The longitude of advertisement
  """
        
  lat = request.args.get('lat')
  lng = request.args.get('lng')
  distance = request.args.get('distance')

  if lat is None or lng is None:
    result = jsonify("Latitude and Longitude could not be empty")
    result.status_code = 400
  else:
    sql = f"""
        SELECT
            description,
            latitude,
            longitude,
            Convert((6371 *
            acos(
                cos (radians({lat})) * cos(radians(latitude)) * cos(radians(longitude) - radians({lng})) +
                sin (radians({lat})) * sin(radians(latitude))
                )
            * 100
            ), UNSIGNED ) AS distance
        FROM advertisements
        HAVING distance < {distance} AND latitude != {lat} AND longitude != {lng}
        ORDER BY distance
        LIMIT 0 , 20;
        """
    db_result = db.session.execute(sql)

    from collections import namedtuple

    Record = namedtuple('Record', db_result.keys())
    records = [Record(*r)._asdict() for r in db_result.fetchall()]

    result = jsonify(records)
    result.status_code = 200

  return result

@app.route("/advertisements", methods=["POST"])
def add_new_advertisement():
  """
  add new advertisement
  ---
  tags:
    - advertisement
  parameters:
    - name: description
      in: body
      type: string
      required: true
      description: description of advertisement
      
    - name: email
      in: body
      type: email
      required: true
      description: email address of user
    
    - name: latitude
      in: body
      type: float
      required: true
      description: latitude of advertisement
      
    - name: longitude
      in: body
      type: float
      required: true
      description: longitute of advertisement
      
    - name: start_time
      in: body
      type: string
      required: false
      description: start time of advertisement
      
    - name: end_time
      in: body
      type: string
      required: false
      description: end time of advertisement
      
    - name: tags
      in: body
      type: string
      required: false
      description: tag list of advertisement
  responses:
    400:
      description: missing some parameters
    200:
      description: successfully add new advertisement
  """
  
  import time

  for k, v in request.json.items():
      if(k == "email"):
          email = v
      elif(k == "description"):
          description = v
      elif(k == "latitude"):
          latitude = v
      elif(k == "longitude"):
          longitude = v
      elif(k == "start_time"):
          start_time = time.strftime('%Y-%m-%d %H:%M:%S')
      elif(k == "end_time"):
          end_time = time.strftime('%Y-%m-%d %H:%M:%S')
      elif(k == "tags"):
          recieved_tags = v
      else:
          print(f"{k}, {v}")

  usr = users_model.User.query.filter(
      users_model.User.email == email
  ).first()

  if(usr):
      new_adv = advertisements_model.Advertisement(user_id=usr.id,
                                            description=description,
                                            latitude=latitude,
                                            longitude=longitude,
                                            start_time=start_time,
                                            end_time=end_time)
      db.session.add(new_adv)
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

        new_adv_tag = advertisement_tags_model.AdvertisementTag(advertisement_id=new_adv.id, tag_id=tag_id)
        db.session.add(new_adv_tag)
        db.session.commit()

      result = jsonify("advertisement successfully created")
  else:
      result = jsonify("User with this email is not available")
      result.status_code = 400

  return result
