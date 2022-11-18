"""This unit contains a business logic processing user's requests on /movies/
route"""
from dao.movie import MovieDAO
from dao.model.movie import MovieSchema
# -------------------------------------------------------------------------


class MovieService:
    """The MovieService class provides all necessary logic to work with
    a movie table"""
    def __init__(self, dao: MovieDAO, schema: MovieSchema) -> None:
        """Initialization of the MovieService class

        :param dao: a MovieDAO instance
        :param schema: a MovieSchema instance
        """
        self.dao = dao
        self.schema = schema

    def get_one(self, bid: int) -> tuple:
        """This method returns a single movie found by its id

        :param bid: an id of searching movie

        :returns:
            a tuple with a dictionary and a status code of the operation
        """
        movie_model = self.dao.get_one(bid)

        if not movie_model:
            return 'Not Found', 404

        return self.schema.dump(movie_model), 200

    def get_all(self, filters: dict) -> tuple:
        """This method returns a list of all movies

        :param filters: a dictionary with searching parameters

        :returns:
            a tuple with a list of movies and a status code of the operation
        """
        if filters.get("director_id") is not None:
            movies = self.dao.get_by_director_id(filters.get("director_id"))
        elif filters.get("genre_id") is not None:
            movies = self.dao.get_by_genre_id(filters.get("genre_id"))
        elif filters.get("year") is not None:
            movies = self.dao.get_by_year(filters.get("year"))
        else:
            movies = self.dao.get_all()

        if not movies:
            return 'Not Found', 404

        movies_list = self.schema.dump(movies, many=True)

        return movies_list, 200

    def create(self, movie_d: dict) -> tuple:
        """This method serves to create a new movie by provided dictionary

        :param movie_d: a dictionary with new movie's data

        :returns:
            a tuple with a result of the operation
        """
        try:
            result = self.dao.create(movie_d)

        except Exception as e:
            print(f'При создании новой записи возникла ошибка {e}')
            return 'Bad Request', 400

        location = {'location': f'/movies/{result.id}'}

        return self.schema.dump(result), 201, location

    def update(self, movie_id: int, movie_d: dict) -> tuple:
        """The method serves to update existing movie

        :param movie_id: the id of the updated movie
        :param movie_d: a dictionary with movie's data to update

        :returns:
            a tuple with a result of the operation
        """
        movie_model = self.dao.get_one(movie_id)

        if not movie_model:
            return 'Not Found', 404

        if 'id' not in movie_d:
            movie_d['id'] = movie_id

        try:
            updated = self.dao.update(movie_model, movie_d)

        except Exception as e:
            print(f'Ошибка при обновлении данных - {e}')
            return 'Bad Request', 400

        return self.schema.dump(updated), 204

    def delete(self, rid: int) -> tuple:
        """This method serves to delete a movie from the movie table

        :param rid: the id of the deleted movie

        :returns:
            a tuple with a result of the operation
        """
        deleted = self.dao.get_one(rid)

        if not deleted:
            return 'Not Found', 404

        result = self.dao.delete(deleted)

        return self.schema.dump(result), 204
