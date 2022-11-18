"""This unit contains the Director and the DirectorSchema classes to work
with data from director table"""
from marshmallow import Schema, fields
from setup_db import db
# -------------------------------------------------------------------------


class Director(db.Model):
    """The Director class represents a model to work with the director
    table"""
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    """The DirectorSchema class is a schema to serialize and deserialize
    director models"""
    id = fields.Int()
    name = fields.Str()
