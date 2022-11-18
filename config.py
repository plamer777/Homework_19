"""This file contains the Config class providing settings for the Flask app"""


class Config(object):
    """The Config class contains all necessary settings for the Flask and
    SQLAlchemy instances"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movies.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
