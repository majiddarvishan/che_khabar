from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from flask_app import db
from .users_model import User

class FollowingUser(db.Model):
    """Data model for user tags."""

    __tablename__ = "following_users"
    follower_user_id = db.Column(db.BigInteger, ForeignKey('users.id'), primary_key=True)
    followed_user_id = db.Column(db.BigInteger, ForeignKey('users.id'), primary_key=True)    
    
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
        return f"""follower_user_id = {self.follower_user_id},
                   followed_user_id = {self.followed_user_id}
                """

    def create_json(self):
        query_object = dict()
        
        query_object["follower_user_id"] = self.follower_user_id 
        query_object["followed_user_id"] = self.followed_user_id

        return query_object
