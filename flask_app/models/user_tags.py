from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from flask_app import db
from .tags import Tag
from .users import User

class UsertTag(db.Model):
    """Data model for user tags."""

    __tablename__ = "user_tags"
    user_id = db.Column(db.BigInteger, ForeignKey('users.id'), primary_key=True)
    tag_id = db.Column(db.BigInteger, ForeignKey('tags.tag_id'), primary_key=True)    
    
    # tag_f_key = relationship(
    #     Tag,
    #     backref=backref('tags',
    #                      uselist=True,
    #                      cascade='delete,all'))
    
    # user_f_key = relationship(
    #     User,
    #     backref=backref('users',
    #                      uselist=True,
    #                      cascade='delete,all'))
    
    def __repr__(self):
        return f"""user_id = {self.user_id},
                   tag_id = {self.tag_id}
                """

    def create_json(self):
        query_object = dict()
        
        query_object["user_id"] = self.user_id 
        query_object["tag_id"] = self.tag_id

        return query_object
