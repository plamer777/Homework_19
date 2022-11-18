"""The unit contains the User class serving as a model to work with the database
and the UserSchema class to serialize and deserialize models"""
from marshmallow import Schema, fields
from setup_db import db
# -------------------------------------------------------------------------


class User(db.Model):
    """The User class represents a model to work with the user table"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    role = db.Column(db.String(20))


class UserSchema(Schema):
    """The UserSchema class represents a schema to serialize and deserialize
    user models"""
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()
    role = fields.Str()