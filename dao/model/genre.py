"""This unit contains Genre and GenreSchema classes those are the model and the
schema to work with a genre table"""
from marshmallow import Schema, fields
from setup_db import db
# ------------------------------------------------------------------------


class Genre(db.Model):
    """The Genre class is a model to work with a genre table"""
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    """The GenreSchema class is a schema to serialize and deserialize
    genre models"""
    id = fields.Int()
    name = fields.Str()
