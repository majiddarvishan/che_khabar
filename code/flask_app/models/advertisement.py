"""Data models."""
from flask_app import db

from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from .user import User

class Advertisement(db.Model):
    """Data model for Advertisement."""

    __tablename__ = "advertisements"
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, ForeignKey('users.id'), nullable=False)
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

    def create_json(self):
        query_object = dict()
        
        query_object["id"] = self.id
        query_object["user_id"] = self.user_id
        query_object["description"] = self.description
        query_object["latitude"] = self.latitude
        query_object["longitude"] = self.longitude
        query_object["start_time"] = self.start_time
        query_object["end_time"] = self.end_time
        query_object["tags"] = self.tags

        return query_object

