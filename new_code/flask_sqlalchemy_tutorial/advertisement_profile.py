from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask import request, make_response

from .models import Advertisement, db

class AdvertisementProfile(Resource):
    def get(self, advertisement_id = None):
        if(advertisement_id):
            adv = Advertisement.query.filter(
                Advertisement.id == advertisement_id
            ).first()

            resp = jsonify(adv.create_json())
            resp.status_code = 200
        else:
            advs = Advertisement.query.all()
            l = list()
            for adv in advs:
                l.append(adv.create_json())

            resp = jsonify(l)
            resp.status_code = 200

        return resp

    def post(self):
        import time

        for k, v in request.json.items():
            if(k == "user_id"):
                user_id = v
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

        new_adv = Advertisement(user_id=user_id,
                    description=description,
                    latitude=latitude,
                    longitude=longitude,
                    start_time=start_time,
                    end_time=end_time,
                    tags=tags
                    )
        db.session.add(new_adv)
        db.session.commit()

        return make_response(f"advertisement successfully created!")