from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask import request, make_response

from .models import Advertisement, User, db

class AdvertisementProfile(Resource):
    def get(self):
        email = request.args.get("email")
        user = User.query.filter(
                User.email == email
            ).first()

        if(user):
            advs = Advertisement.query.filter(
                Advertisement.user_id == user.id
            ).all()

            l = list()
            for adv in advs:
                l.append(adv.create_json())

            result = jsonify(l)

        else:
            result = jsonify("User with this email is not available") 
            result.status_code = 400
        
        return result

    def post(self):
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
                tags = v
            else:
                print(f"{k}, {v}")

        user = User.query.filter(
                User.email == email
            ).first()

        if(user):
            new_adv = Advertisement(user_id=user.id,
                        description=description,
                        latitude=latitude,
                        longitude=longitude,
                        start_time=start_time,
                        end_time=end_time,
                        tags=tags
                        )
            db.session.add(new_adv)
            db.session.commit()

            result = jsonify("advertisement successfully created") 
        else:
            result = jsonify("User with this email is not available") 
            result.status_code = 400

        return result