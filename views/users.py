"""The unit contains a CBVs to with routes like '/users/ and /users/1"""
from flask_restx import Resource, Namespace
from flask import request
from implemented import user_service, auth_service
# -----------------------------------------------------------------------
user_ns = Namespace('users')
# -----------------------------------------------------------------------


@user_ns.route('/')
class UsersView(Resource):
    """The UsersView is a CBV to process requests like /users/"""
    @auth_service.admin_required
    def get(self):
        """This method process GET requests

        :returns: a result of the request
        """
        return user_service.get_all()

    def post(self):
        """This method process POST requests

        :returns: a result of the request
        """
        user_data = request.json

        return user_service.add_new(user_data)


@user_ns.route('/<int:user_id>')
class UserView(Resource):
    """The UserView is a CBV to process requests like /users/{user_id}"""
    @auth_service.auth_required
    def get(self, user_id: int):
        """This method process GET requests

        :returns:
            a result of the request
        """
        user = user_service.get_by_id(user_id)

        return user

    @auth_service.auth_required
    def put(self, user_id: int):
        """This method process PUT requests

        :param user_id: an id of the user to update

        :returns:
            a result of the request
        """
        user_data = request.json

        return user_service.update_data(user_id, user_data)

    @auth_service.auth_required
    def delete(self, user_id: int):
        """This method process DELETE requests

        :param user_id: an id of the user to delete

        :returns:
            a result of the request
        """
        return user_service.delete(user_id)
