"""This unit contains CBVs to process requests like /directors/,
/directors/{rid}"""
from flask import request
from flask_restx import Resource, Namespace
from implemented import director_service, auth_service
# ------------------------------------------------------------------------
director_ns = Namespace('directors')
# ------------------------------------------------------------------------


@director_ns.route('/')
class DirectorsView(Resource):
    """The DirectorsView is a CBV to process requests like /movies/"""
    @auth_service.auth_required
    def get(self):
        """This method serves to work with GET requests

        :returns:
            a result of the GET request
        """
        directors = director_service.get_all()

        return directors

    @auth_service.admin_required
    def post(self):
        """This method serves to work with POST requests

        :returns:
            a result of the POST request with location header
        """
        new_director = request.json

        result = director_service.create(new_director)

        return result


@director_ns.route('/<int:rid>')
class DirectorView(Resource):
    """The DirectorView is a CBV to process requests like /directors/{rid}"""
    @auth_service.auth_required
    def get(self, rid: int):
        """This method serves to work with GET requests

        :param rid: the id of the searching director

        :returns:
            a result of the GET request
        """
        director = director_service.get_one(rid)

        return director

    @auth_service.admin_required
    def put(self, rid: int):
        """This method serves to work with PUT requests

        :param rid: the id of the updating director

        :returns:
            a result of the PUT request
        """
        new_data = request.json

        result = director_service.update(rid, new_data)

        return result

    @auth_service.admin_required
    def delete(self, rid: int):
        """This method serves to work with DELETE requests

        :param rid: the id of the deleting director

        :returns:
            a result of the DELETE request
        """
        result = director_service.delete(rid)

        return result
