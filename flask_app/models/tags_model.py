from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from flask_app import db

class Tag(db.Model):
    """Data model for tags."""

    __tablename__ = "tags"
    tag_id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True, nullable=False)
    
    def __repr__(self):
        return f"""tag_id = {self.tag_id},
                   name = {self.name}
                """

    def create_json(self):
        query_object = dict()
        
        query_object["tag_id"] = self.tag_id
        query_object["name"] = self.name 

        return query_object
