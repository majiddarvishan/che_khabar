"""Data models."""
from . import db

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    firstname = db.Column(db.String(64), index=False, nullable=False)
    lastname = db.Column(db.String(64), index=False, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    mobile = db.Column(db.Numeric(20), index=True, unique=True, nullable=False)
    created = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    bio = db.Column(db.UnicodeText, index=False, unique=False, nullable=True)
    distance = db.Column(db.SmallInteger, index=False, unique=False, nullable=True)
    tags = db.Column(db.Text, index=False, unique=False, nullable=True)

    def __repr__(self):
        return f"""firstname = {self.firstname},
                   lastname = {self.lastname},
                   email = {self.email},
                   mobile = {self.mobile},
                   created = {self.created},
                   distance = {self.distance}
                """

    def create_json(self):
        # query_object = OrderedDict([("user_id",  self.user_id),
        #                     ("user_name",  self.user_name ),
        #                     ("user_mobile",  self.user_mobile),
        #                     ("distance",  self.distance),
        #                     ("tags",  self.tags )])

        query_object = dict()
        
        # query_object["user_id"] = self.user_id
        query_object["first_name"] = self.firstname
        query_object["last_name"] = self.lastname 
        query_object["email"] = self.email 
        query_object["mobile"] = self.mobile
        query_object["distance"] = self.distance
        query_object["tags"] = self.tags 

        return query_object

class Advertisement(db.Model):
    """Data model for Advertisement."""

    __tablename__ = "advertisements"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, ForeignKey('users.id'))
    description = db.Column(db.UnicodeText, index=False, nullable=False)
    latitude = db.Column(db.FLOAT, index=False, nullable=False)
    longitude = db.Column(db.FLOAT, index=False, nullable=False)
    start_time = db.Column(db.DateTime, default=func.now(), index=False, unique=False, nullable=True)
    end_time = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    tags = db.Column(db.Text, index=False, unique=False, nullable=True)

     # Use cascade='delete,all' to propagate the deletion of a Department onto its Employees
    users = relationship(
        User,
        backref=backref('users',
                         uselist=True,
                         cascade='delete,all'))
 

    def __repr__(self):
        return f"""id = {self.id},
                   user_id = {self.user_id},
                   description = {self.description},
                   latitude = {self.latitude},
                   longitude = {self.longitude},
                   start_time = {self.start_time},
                   end_time = {self.end_time}
                """

#     def create_json(self):
#         # query_object = OrderedDict([("user_id",  self.user_id),
#         #                     ("user_name",  self.user_name ),
#         #                     ("user_mobile",  self.user_mobile),
#         #                     ("distance",  self.distance),
#         #                     ("tags",  self.tags )])

#         query_object = dict()
        
#         # query_object["user_id"] = self.user_id
#         query_object["first_name"] = self.firstname
#         query_object["last_name"] = self.lastname 
#         query_object["email"] = self.email 
#         query_object["mobile"] = self.mobile
#         query_object["distance"] = self.distance
#         query_object["tags"] = self.tags 

#         return query_object

