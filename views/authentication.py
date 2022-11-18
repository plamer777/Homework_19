"""This unit contains the CBV to authenticate users"""
from flask import request
from flask_restx import Resource, Namespace
from implemented import auth_service
# ------------------------------------------------------------------------
auth_ns = Namespace('auth')
# ------------------------------------------------------------------------


@auth_ns.route('/')
class AuthenticationView(Resource):
    """The AuthenticationView is a CBV to process requests like /auth/"""
    def post(self):
        """The method processes POST requests

        :returns:
            a dictionary with access token and refresh token or an
        error message if authentication was not successful
        """
        user_data = request.json

        return auth_service.authenticate_user(user_data)

    def put(self):
        """The method processes PUT requests

        :returns:
            a dictionary with access token and refresh token or an
        error message if decoding refresh token was failed
        """
        user_data = request.json

        return auth_service.authenticate_user(user_data, is_refresh=True)



