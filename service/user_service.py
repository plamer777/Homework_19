"""There is a UserService class in the unit containing all necessary business
logic to work with users table of the database"""
import hashlib
import base64
import hmac
from constants import HASH_ALGO, HASH_SALT, HASH_ITERATIONS, REQUIRED_KEYS
from dao.model.user import UserSchema
from dao.user_dao import UserDao
# ------------------------------------------------------------------------
from setup_db import db


class UserService:
    """The UserService class contains all methods to work with users table"""
    def __init__(self, dao: UserDao, schema: UserSchema) -> None:
        """The initialization method of the UserService class

        :param dao: an instance of UserDao class
        :param schema: an instance of UserSchema
        """
        self._dao = dao
        self._schema = schema

    def get_all(self) -> tuple:
        """This method returns a list of all users

        :return: a tuple containing the list of users and a status code
        """
        all_users = self._dao.get_all()

        if not all_users:
            return 'Not Found', 404

        users_list = self._schema.dump(all_users, many=True)

        return users_list, 200

    def get_by_id(self, user_id: int) -> tuple:
        """This method returns a user by id

        :param user_id: the id of the searching user

        :returns: a tuple with the dictionary or string and a status code
        """
        user = self._dao.get_by_id(user_id)

        if not user:
            return 'Not Found', 404

        return self._schema.dump(user), 200

    def get_by_name(self, name: str) -> tuple:
        """This method returns a user found by name

        :param name: the name of the searching user

        :returns: a tuple with the dictionary or string and a status code
        """
        found_user = self._dao.get_by_name(name)

        if not found_user:
            return 'Not Found', 404

        return self._schema.dump(found_user), 200

    def add_new(self, user_data: dict) -> tuple:
        """This method adds a new user to the users table

        :param user_data: the dictionary with the user data to add

        :returns: a tuple with a result of the operation
        """
        if not self.check_data(user_data):
            return 'Bad request', 400

        if self._dao.get_by_name(user_data.get('username')):
            return 'The user already exists', 400

        user_data['password'] = self._encode_password(
            user_data['password'])

        result = self._dao.create(user_data)
        location = {'location': f'/users/{result.id}'}

        return 'Created', 201, location

    def update_data(self, user_id: int, user_data: dict) -> tuple:
        """This method updates the user data in the users table

        :param user_id: the id of the user to update
        :param user_data: the dictionary with the user's data

        :returns: a tuple with a result of the operation
        """
        # checking a data provided by the user
        if not self.check_data(user_data):
            return 'Bad request', 400

        existing_user = self._dao.get_by_name(user_data.get('username'))

        # if there is another user with the same username then restrict
        # the action
        if existing_user and existing_user.id != user_id:
            return 'This nickname is already used by another user', 400

        # encoding user password
        user_data['password'] = self._encode_password(user_data['password'])

        self._dao.update(user_id, user_data)

        return '', 204

    def delete(self, user_id: int) -> tuple:
        """This method deletes a user from the users table

        :param user_id: the id of the user to delete

        :returns: a tuple with a result of the operation
        """
        deleted_user = self._dao.get_by_id(user_id)

        if not deleted_user:
            return 'Not Found', 404

        self._dao.delete(deleted_user)

        return '', 204

    def authenticate(self, user_data: dict) -> tuple:
        """This method authenticates a user

        :param user_data: a dictionary containing user's information

        :returns: a tuple with a result of the operation. If authentication
        was successful then the tuple contains a dictionary with full
        user information such as id, username, password and role
        """
        try:
            username = user_data['username']
            password = user_data['password']

        except Exception as e:
            print(f'Ошибка при получении имени пользователя или пароля {e}')
            return 'Bad Request', 400

        user = self._dao.get_by_name(username)

        # checking if the user exists
        if not user:
            return 'The user is not registered', 401

        # checking if the provided password is correct
        elif not self._check_password(password, user.password):
            return 'The password is wrong', 401

        return self._schema.dump(user), 201

    @staticmethod
    def _encode_password(password: str) -> bytes:
        """This method serves to encode a password

        :param password: a string to encode

        :returns: a string with the encoded password
        """
        # turning up the string into bytes
        password = password.encode('utf-8')
        encoded_password = hashlib.pbkdf2_hmac(HASH_ALGO, password,
                                               HASH_SALT, HASH_ITERATIONS)

        return base64.b64encode(encoded_password)

    def _check_password(self, provided: str, validated: str) -> bool:
        """This method serves to validate the provided password

        :param provided: a string with the provided password
        :param validated: a string with the password taken from the database

        :returns: a boolean indicating if the provided password is valid
        """
        provided = base64.b64decode(self._encode_password(provided))
        validated = base64.b64decode(validated)

        return hmac.compare_digest(provided, validated)

    @staticmethod
    def check_data(user_data: dict) -> bool:
        """This method serves to check a dictionary with user's data

        :param user_data: a dictionary with user's data

        :returns: a boolean indicating the result of the checking
        """
        # if user_data is empty then it's invalid
        if not user_data:
            return False

        # if user data haven't necessary keys then data isn't valid
        if not REQUIRED_KEYS.issubset(set(user_data)):
            return False

        for key, value in user_data.items():
            # if dictionary value is empty then data isn't valid, excepting the
            # 'role' key
            if not value:
                if key == 'role':
                    user_data[key] = 'user'
                else:
                    return False
        return True
