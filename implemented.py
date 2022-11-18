"""This unit provides an instances to serve the Flask application"""
from dao.director import DirectorDAO
from dao.genre import GenreDAO
from dao.model.user import UserSchema
from dao.movie import MovieDAO
from dao.user_dao import UserDao
from service.director import DirectorService, DirectorSchema
from service.genre import GenreService, GenreSchema
from service.movie import MovieService, MovieSchema
from service.user_service import UserService
from service.auth_service import AuthService
from setup_db import db
# ------------------------------------------------------------------------

director_dao = DirectorDAO(session=db.session)
genre_dao = GenreDAO(session=db.session)
movie_dao = MovieDAO(session=db.session)
user_dao = UserDao(db.session)

director_service = DirectorService(dao=director_dao, schema=DirectorSchema())
genre_service = GenreService(dao=genre_dao, schema=GenreSchema())
movie_service = MovieService(dao=movie_dao, schema=MovieSchema())
user_service = UserService(user_dao, UserSchema())
auth_service = AuthService(user_service)
