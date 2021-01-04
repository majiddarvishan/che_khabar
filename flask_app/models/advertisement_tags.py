from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func
from sqlalchemy.orm import relationship, backref

from flask_app import db
from .tags import Tag
from .advertisements import Advertisement

class AdvertisementTag(db.Model):
    """Data model for advertisement tags."""

    __tablename__ = "advertisement_tags"
    advertisement_id = db.Column(db.BigInteger, ForeignKey('advertisements.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.BigInteger, ForeignKey('tags.tag_id'), primary_key=True, nullable=False)

    tag_f_key = relationship(
        Tag,
        backref=backref('tags',
                         uselist=True,
                         cascade='delete,all'))

    advertisement_f_key = relationship(
        Advertisement,
        backref=backref('advertisements',
                         uselist=True,
                         cascade='delete,all'))

    def __repr__(self):
        return f"""advertisement_id = {self.advertisement_id},
                   tag_id = {self.tag_id}
                """

    def create_json(self):
        query_object = dict()

        query_object["advertisement_id"] = self.advertisement_id
        query_object["tag_id"] = self.tag_id

        return query_object
