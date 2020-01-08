from flask_restful import Resource, Api
from flask_jsonpify import jsonify
from flask import request

from collections import OrderedDict

from database import Database

class Advertisement(Resource):
    def __init__(self):
        self.id = 0
        self.advertiser_id = 0
        self.body = ""
        self.latitude = 0.0
        self.longitude = 0.0
        self.start_date = 0
        self.end_date = 0
        self.tags = ""

    def _create_json(self):
        # query_object = OrderedDict([("user_id",  self.user_id),
        #                     ("user_name",  self.user_name ),
        #                     ("user_mobile",  self.user_mobile),
        #                     ("distance",  self.distance),
        #                     ("tags",  self.tags )])

        query_object = dict()
        
        query_object["id"] = self.id
        query_object["advertiser_id"] = self.advertiser_id 
        query_object["body"] = self.body
        query_object["latitude"] = self.latitude
        query_object["longitude"] = self.longitude
        query_object["start_date"] = self.start_date
        query_object["end_date"] = self.end_date
        query_object["tags"] = self.tags 

        return query_object

    def dump(self):
        print(f"""id = {self.id},
                  advertiser_id = {self.advertiser_id},
                  body = {self.body},
                  latitude = {self.latitude},
                  longitude = {self.longitude}, 
                  start_date = {self.start_date}, 
                  end_date = {self.end_date}, 
                  tags = {self.tags}""")
    def get(self, id):
        db = Database()
        db.read(self, id)

        # self.dump()
        
        resp = jsonify(self._create_json())
        resp.status_code = 200

        return resp

        # return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches 

    def post(self):
        import time  
        result = {"message": "ok"}

        try:
            for k, v in request.json.items():
                if(k == "advertiser_id"):
                    self.advertiser_id = v
                elif(k == "body"):
                    self.body = v
                elif(k == "latitude"):
                    self.latitude = v
                elif(k == "longitude"):
                    self.longitude = v
                elif(k == "start_date"):
                    self.start_date = time.strftime('%Y-%m-%d %H:%M:%S')
                elif(k == "end_date"):
                    self.end_date = time.strftime('%Y-%m-%d %H:%M:%S')
                elif(k == "tags"):
                    self.tags = v
                else:
                    print(f"{k}, {v}")
                
            db = Database()
            db.save_advertise_data(self)

        except Exception as e:
            print(e)
            result = {"message": str(e)}

        return jsonify(result)
