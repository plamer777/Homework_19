"""This unit contains the DirectorDAO class to work with a director table"""
from dao.model.director import Director
# ------------------------------------------------------------------------


class DirectorDAO:
    """The DirectorDAO class provides all necessary methods to work with
    the director table"""
    def __init__(self, session) -> None:
        """This is a constructor for the DirectorDAO class

        :param session: the current db session
        """
        self.session = session

    def get_one(self, bid: int) -> Director:
        """This method returns a single director found by the given bid

        :param bid: the id of the searching director

        :returns:
            an instance of the Director class
        """
        return self.session.query(Director).get(bid)

    def get_all(self) -> list:
        """This method returns a list of all directors found in the
        director table

        :returns:
            a list of Director instances
        """
        return self.session.query(Director).all()

    def create(self, director_d: dict) -> Director:
        """This method serves to add a new record in the director table

        :param director_d: a dictionary with the new director's data

        :returns:
            an instance of the Director class
        """
        ent = Director(**director_d)

        self.session.add(ent)
        self.session.commit()

        return ent

    def delete(self, director: Director) -> Director:
        """This method removes a record from the director table

        :param director: a Director class instance

        :returns:
            an instance of the Director class that was removed
        """
        self.session.delete(director)
        self.session.commit()

        return director

    def update(self, director: Director, director_d: dict) -> Director:
        """This method updates a record in the director table

        :param director: a Director class instance
        :param director_d: a dictionary with updated data

        :returns:
            an instance of the Director class that was updated
        """
        director.name = director_d.get("name")

        self.session.add(director)
        self.session.commit()

        return director
