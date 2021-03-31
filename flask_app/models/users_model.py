"""Data models."""
from flask_app import db

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Enum
from sqlalchemy.orm import relationship, backref
import datetime
import enum

class UserMode(enum.Enum):
    Common = 1
    Advertiser = 2
    
class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.BigInteger, primary_key=True)
    firstname = db.Column(db.String(64), index=False, nullable=False)
    lastname = db.Column(db.String(64), index=False, nullable=False)
    nickname = db.Column(db.String(64), index=False, nullable=True)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    mobile = db.Column(db.Numeric(20), index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), index=False, unique=False, nullable=False)
    active = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, index=False, unique=False, nullable=True)
    visible = db.Column(db.Boolean, default=True)
    distance = db.Column(db.SmallInteger, index=False, unique=False, nullable=True)
    user_mode = db.Column(Enum(UserMode), index=False, unique=False, nullable=False)
    bio = db.Column(db.UnicodeText, index=False, unique=False, nullable=True)

    def __repr__(self):
        return f"""firstname = {self.firstname},
                   lastname = {self.lastname},
                   nicktname = {self.nickname},
                   email = {self.email},
                   mobile = {self.mobile},
                   created_at = {self.created_at},
                   active = {self.active},
                   score = {self.score},
                   visible = {self.visible},
                   distance = {self.distance},
                   bio = {self.bio}
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
        query_object["nickname"] = self.nickname
        query_object["email"] = self.email
        query_object["mobile"] = self.mobile
        query_object["created_at"] = self.created_at
        query_object["active"] = self.active
        query_object["score"] = self.score
        query_object["visible"] = self.visible        
        query_object["distance"] = self.distance
        query_object["bio"] = self.bio

        return query_object