"""There is the UserDao class in the unit that allows access to the user
table in the database"""
from dao.model.user import User
from setup_db import db
# ------------------------------------------------------------------------


class UserDao:
    """The UserDao class contains a base logic to get access to the user
    table"""
    def __init__(self, session: db.session) -> None:
        """Initialization of the UserDao class

        :param session: the current session object
        """
        self.session = session

    def get_all(self) -> list:
        """The method returns a list of users found in the database

        :returns: a list of models
        """
        return self.session.query(User).all()

    def get_by_id(self, user_id: int) -> User:
        """The method returns a user found by the given user_id

        :param user_id: the id of the searching user

        :returns: a user model found by the given id
        """
        return self.session.query(User).get(user_id)

    def get_by_name(self, name: str) -> User:
        """The method returns a user found by the given name

        :param name: the name of the searching user

        :returns: a user model found by the given name
        """
        return self.session.query(User).filter(User.username == name).first()

    def create(self, user_data: dict) -> User:
        """The method creates a new record in the user table

        :param user_data: a dictionary containing a user's information

        :returns: a user model created by provided user_data
        """
        new_user = User(**user_data)

        self.session.add(new_user)
        self.session.commit()

        return new_user

    def update(self, user_id: int, user_data: dict) -> None:
        """This method updates a user's data in the user table

        :param user_id: the id of the user to update
        :param user_data: a dictionary containing user's information
        """
        self.session.query(User).filter(
            User.id == user_id).update(user_data)
        self.session.commit()
        self.session.close()

    def delete(self, user: User) -> None:
        """This method deletes a user from the user table

        :param user: an instance of User class to delete
        """
        self.session.delete(user)
        self.session.commit()
        self.session.close()
