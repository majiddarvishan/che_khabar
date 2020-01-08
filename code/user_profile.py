from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask import request

from collections import OrderedDict

import database

class UserProfile(Resource):
    def __init__(self):
        self.user_id = 0
        self.user_name = ""
        self.user_password = "" 
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
        
        query_object["user_id"] = self.user_id
        query_object["user_name"] = self.user_name 
        query_object["user_mobile"] = self.user_mobile
        query_object["distance"] = self.distance
        query_object["tags"] = self.tags 

        return query_object

    def dump(self):
        print(f"""user_id = {self.user_id},
                  user_name = {self.user_name},
                  password = {self.user_password},
                  mobile = {self.user_mobile},
                  distance = {self.distance}, 
                  tags = {self.tags}""")

    def get(self, user_id):
        lat = request.args.get('lat')
        lng = request.args.get('lng')
        
        if lat is None or lng is None:
            database.read(self, user_id)
    
            resp = jsonify(self._create_json())
            resp.status_code = 200
        else:
            database.read(self, user_id)
            results = database.find_nearest_points(lat, lng, self.distance)

            resp = jsonify(results)
            resp.status_code = 200

        return resp

        # return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches 

    def post(self): 
        result = {"message": "ok"}

        try:
            for k, v in request.json.items():
                if(k == "user_name"):
                    self.user_name = v
                elif(k == "password"):
                    self.user_password = v
                elif(k == "mobile"):
                    self.user_mobile = v
                elif(k == "distance"):
                    self.distance = v
                elif(k == "tags"):
                    self.tags = v
                else:
                    print(f"{k}, {v}")
                
            database.save_user_data(self)

        except Exception as e:
            print(e)
            result = {"message": str(e)}

        return jsonify(result)
