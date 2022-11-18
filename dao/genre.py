"""This unit contains a GenreDAO class to work with a genre table"""
from dao.model.genre import Genre
# --------------------------------------------------------------------------


class GenreDAO:
    """The GenreDAO class provides access to the genre table"""
    def __init__(self, session) -> None:
        """Initialization of the GenreDAO class

        :param session: the current db session
        """
        self.session = session

    def get_one(self, bid: int) -> Genre:
        """This method returns a single genre found by the given bid

        :param bid: an id of the searching genre

        :returns:
            a Genre instance
        """
        return self.session.query(Genre).get(bid)

    def get_all(self) -> list:
        """This method returns a list of genres

        :returns:
            a list of Genre instances
        """
        return self.session.query(Genre).all()

    def create(self, genre_d: dict) -> Genre:
        """This method creates a new record in the genre table

        :param genre_d: a dictionary with new movie's data

        :returns:
            a created Genre instance
        """
        ent = Genre(**genre_d)

        self.session.add(ent)
        self.session.commit()

        return ent

    def delete(self, genre: Genre) -> Genre:
        """This method deletes a genre from a genre table

        :param genre: a Genre instance

        :returns:
            a deleted Genre instance
        """
        self.session.delete(genre)
        self.session.commit()

        return genre

    def update(self, genre: Genre, genre_d: dict) -> Genre:
        """This method updates a genre in a genre table

        :param genre: a Genre instance
        :param genre_d : a dictionary with movie's data to update

        :returns:
            an updated Genre instance
        """
        genre.name = genre_d.get("name")

        self.session.add(genre)
        self.session.commit()

        return genre

