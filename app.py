"""This is a main file to run the Flask application"""
from flask import Flask
from flask_restx import Api
from config import Config
from setup_db import db
from views.directors import director_ns
from views.genres import genre_ns
from views.movies import movie_ns
from views.users import user_ns
from views.authentication import auth_ns
# ---------------------------------------------------------------------------


def create_app(config_object):
    """This function serves to create the Flask application

    :param config_object: an instance of Config class with necessary settings

    :returns: an instance of the Flask
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    """This function creates Api instance, configure database object and
    register namespaces

    :param app: a configured instance of the Flask
    """
    db.init_app(app)
    api = Api(app)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(movie_ns)
    api.add_namespace(user_ns)
    api.add_namespace(auth_ns)
# ---------------------------------------------------------------------------


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
