"""This unit contains CBVs to process requests like /movies/ and /movies/1"""
from flask import request
from flask_restx import Resource, Namespace
from implemented import movie_service, auth_service
# -----------------------------------------------------------------------
movie_ns = Namespace('movies')
# -----------------------------------------------------------------------


@movie_ns.route('/')
class MoviesView(Resource):
    """The MoviesView is a CBV to process requests like /movies/"""
    @auth_service.auth_required
    def get(self):
        """This method processes GET requests

        :returns:
            a result of the GET request
        """
        director = request.args.get("director_id")
        genre = request.args.get("genre_id")
        year = request.args.get("year")
        filters = {
            "director_id": director,
            "genre_id": genre,
            "year": year,
        }

        all_movies = movie_service.get_all(filters)

        return all_movies

    @auth_service.admin_required
    def post(self):
        """This method processes POST requests

        :returns:
            a result of the POST request with 'location' header
        """
        req_json = request.json
        result = movie_service.create(req_json)

        return result


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    """The MovieView is a CBV to process requests like /movies/{bid}"""
    @auth_service.auth_required
    def get(self, bid: int):
        """This method processes GET requests

        :returns:
            a result of the GET request
        """
        movie = movie_service.get_one(bid)

        return movie

    @auth_service.admin_required
    def put(self, bid: int):
        """This method processes PUT requests

        :returns:
            a result of the operation
        """
        req_json = request.json
        result = movie_service.update(bid, req_json)

        return result

    @auth_service.admin_required
    def delete(self, bid: int):
        """This method processes DELETE requests

        :returns:
            a result of the DELETE request
        """
        result = movie_service.delete(bid)

        return result
