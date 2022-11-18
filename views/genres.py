"""This unit contains a CBVs to process requests like /genre/, /genre/{rid}"""
from flask import request
from flask_restx import Resource, Namespace
from implemented import genre_service, auth_service
# -----------------------------------------------------------------------
genre_ns = Namespace('genres')
# -----------------------------------------------------------------------


@genre_ns.route('/')
class GenresView(Resource):
    """The GenresView is a CBV to process requests like /movies/"""
    @auth_service.auth_required
    def get(self):
        """This method processes GET requests

        :returns:
            a result of the GET request
        """
        all_genres = genre_service.get_all()

        return all_genres

    @auth_service.admin_required
    def post(self):
        """This method processes POST requests

        :returns:
            a result of the POST request
        """
        new_genre = request.json

        result = genre_service.create(new_genre)

        return result


@genre_ns.route('/<int:rid>')
class GenreView(Resource):
    """The GenreView is a CBV to process requests like /movies/{rid}"""
    @auth_service.auth_required
    def get(self, rid: int):
        """This method processes GET requests

        :returns:
            a result of the GET request
        """
        found_genre = genre_service.get_one(rid)

        return found_genre

    @auth_service.admin_required
    def put(self, rid: int):
        """This method processes PUT requests

        :returns:
            a result of the PUT request
        """
        new_data = request.json

        result = genre_service.update(rid, new_data)

        return result

    @auth_service.admin_required
    def delete(self, rid: int):
        """This method processes DELETE requests

        :returns:
            a result of the DELETE request
        """
        result = genre_service.delete(rid)

        return result
