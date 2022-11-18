"""This unit contains the AuthService class serving to authenticate users"""
from flask import request
from datetime import datetime, timedelta
import jwt
from flask import abort
from service.user_service import UserService
from constants import SECRET, JWT_ALGO, ACCESS_TIME, REFRESH_TIME
# ----------------------------------------------------------------------


class AuthService:
    """The AuthService class contains a business logic to authenticate users"""
    def __init__(self, service: UserService) -> None:
        """Initialization of the AuthService class

        :param service: the UserService instance
        """
        self._service = service

    def authenticate_user(self, user_data: dict, is_refresh: bool = False):
        """This method serves to authenticate a user and create a token
        by provided user data or refresh token

        :param user_data: the dictionary with user data or refresh token
        :param is_refresh: the flag indicating if it's a token creation by
        user data or a refresh token

        :returns: a tuple containing the result of authentication
        """
        # if a taken creates by user data then we use an authenticate function
        # of service
        if not is_refresh:
            result = self._service.authenticate(user_data)

        # otherwise we decode provided refresh token
        else:
            if 'refresh_token' not in user_data:
                return 'Bad Request', 400

            token_data = self._decode_token(user_data.get('refresh_token'))
            result = self._service.get_by_name(token_data['username'])

        # if there were a problems with authentication then return result
        # describing the problems
        if result[1] not in (201, 200):
            return result

        return self._create_tokens(result[0]), 201

    def auth_required(self, func):
        """This method is a decorator to restrict access to CBVs' methods
        depending on the user's role

        :param func: a function to which access should be restricted

        :returns: a wrapper - the function that wraps restricted function
        """
        def wrapper(*args, **kwargs):
            # receiving a token and user_data from request
            token = request.headers.get('Authorization')
            user_data = request.json
            method = request.method

            # a token's preparation and extracting data
            token = self._check_and_fix_token(token)
            token_data = self._decode_token(token)

            # this branch used only for /user/{user_id} route
            if 'user_id' in kwargs:

                found_user = self._service.get_by_id(kwargs['user_id'])

                if found_user[1] != 200:
                    abort(404)

                # if user found by id isn't one receiving from token then
                # access is restricted but only if the user is not admin
                elif found_user[0].get('username') != token_data.get(
                        'username') and token_data.get('role') != 'admin':
                    abort(403)

                # if user with role "user" tries to change a role of himself
                # then access is restricted
                elif token_data.get('role') == 'user' and method != 'GET':

                    if user_data and user_data.get('role') != 'user':
                        abort(403)

            return func(*args, **kwargs)

        return wrapper

    def admin_required(self, func):
        """This method is a decorator that serves to provide a full access
        only for users having an 'admin' role

        :param func: the function that should be restricted

        :returns: a wrapper - the decorated function
        """
        def wrapper(*args, **kwargs):

            token = request.headers.get('Authorization')

            token = self._check_and_fix_token(token)
            token_data = self._decode_token(token)

            # if user's role is not "admin" then access is restricted
            if token_data.get('role') != 'admin':
                abort(403)

            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def _check_and_fix_token(token: str) -> str:
        """This is a secondary method that helps to prepare a token

        :param token: the token to prepare

        :returns: a token - checked and prepared token
        """
        if not token:
            abort(401)

        try:
            token = token.split('Bearer ')[-1]

        except Exception as e:
            print(f'Ошибка при извлечении токена {e}')
            abort(400)

        return token

    @staticmethod
    def _create_tokens(user_data: dict) -> dict:
        """This method creates a couple of tokens by provided data

        :param user_data: a dictionary with user data

        :returns: a dictionary with access and refresh tokens
        """
        access_time = datetime.utcnow() + timedelta(minutes=ACCESS_TIME)
        refresh_time = datetime.utcnow() + timedelta(days=REFRESH_TIME)

        token_data = {'username': user_data['username'],
                      'role': user_data['role'],
                      'exp': access_time}
        access_token = jwt.encode(token_data, SECRET, algorithm=JWT_ALGO)

        token_data['exp'] = refresh_time
        refresh_token = jwt.encode(token_data, SECRET, algorithm=JWT_ALGO)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    @staticmethod
    def _decode_token(token: str) -> dict:
        """This method decodes a token

        :param token: the token to decode

        :returns: the data extracted from the token or 401-error
        """
        try:
            token_data = jwt.decode(token, SECRET,
                                    algorithms=[JWT_ALGO])

            return token_data

        except Exception as e:
            print(f'Ошибка при декодировании токена: {e}')
            abort(401)
