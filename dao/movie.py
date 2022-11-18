"""This unit contains a MovieDAO class to work with movie table"""
from dao.model.movie import Movie
# -----------------------------------------------------------------------


class MovieDAO:
    """The MovieDAO class provides all methods to work with the movie table"""
    def __init__(self, session) -> None:
        """Initialization of the MovieDAO class

        :param session: the current db session
        """
        self.session = session

    def get_one(self, bid: int) -> Movie:
        """This method returns a single movie found by the given bid

        :param bid: an id of the searching movie

        :returns:
            a Movie instance
        """
        return self.session.query(Movie).get(bid)

    def get_all(self) -> list:
        # А еще можно сделать так, вместо всех методов get_by_*
        # t = self.session.query(Movie)
        # if "director_id" in filters:
        #     t = t.filter(Movie.director_id == filters.get("director_id"))
        # if "genre_id" in filters:
        #     t = t.filter(Movie.genre_id == filters.get("genre_id"))
        # if "year" in filters:
        #     t = t.filter(Movie.year == filters.get("year"))
        # return t.all()

        return self.session.query(Movie).all()

    def get_by_director_id(self, val: int) -> list:
        """This method returns all movies that wos found by the given
        director_id

        :param val: an id of the director to search movie by

        :returns:
            a list of Movie instances
        """
        return self.session.query(Movie).filter(Movie.director_id == val).all()

    def get_by_genre_id(self, val: int) -> list:
        """This method returns all movies found by the given genre_id

        :param val: an id of the genre to search movie by

        :returns:
            a list of Movie instances
        """
        return self.session.query(Movie).filter(Movie.genre_id == val).all()

    def get_by_year(self, val: int) -> list:
        """This method returns all movies found by the given year

        :param val: a year to search movie by

        :returns:
            a list of Movie instances
        """
        return self.session.query(Movie).filter(Movie.year == val).all()

    def create(self, movie_d: dict) -> Movie:
        """This method serves to create a new record in the movie table

        :param movie_d: a dictionary with new movie's data

        :returns:
            an instance of Movie class
        """
        ent = Movie(**movie_d)

        self.session.add(ent)
        self.session.commit()

        return ent

    def delete(self, movie: Movie) -> Movie:
        """This method serves to delete a movie from the movie table

        :param movie: an instance of Movie class

        :returns:
            an instance of Movie class that has been deleted
        """
        self.session.delete(movie)
        self.session.commit()

        return movie

    def update(self, movie: Movie, movie_d: dict) -> Movie:
        """This method serves to update a movie in the movie table

        :param movie: an instance of Movie class
        :param movie_d: dictionary with an updated movie's data

        :returns:
            an instance of Movie class that has been updated
        """
        movie.title = movie_d.get("title")
        movie.description = movie_d.get("description")
        movie.trailer = movie_d.get("trailer")
        movie.year = movie_d.get("year")
        movie.rating = movie_d.get("rating")
        movie.genre_id = movie_d.get("genre_id")
        movie.director_id = movie_d.get("director_id")

        self.session.add(movie)
        self.session.commit()

        return movie
