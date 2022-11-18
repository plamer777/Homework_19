"""This file contains the GenreService class provides a business logic to
work with the genre table"""
from dao.genre import GenreDAO
from dao.model.genre import GenreSchema
# --------------------------------------------------------------------------


class GenreService:
    """The GenreService class provides a business logic to work with a
    genre table"""
    def __init__(self, dao: GenreDAO, schema: GenreSchema) -> None:
        """This method initializes the GenreService class

        :param dao: the GenreDAO instance
        :param schema: the GenreSchema instance
        """
        self.dao = dao
        self.schema = schema

    def get_one(self, bid: int) -> tuple:
        """This method returns a single genre found by the given bid

        :param bid: the id of the searching genre

        :returns:
            a tuple containing a dictionary with genre data and a status
            code of the operation
        """
        genre_model = self.dao.get_one(bid)

        if not genre_model:
            return 'Not Found', 404

        genre_dict = self.schema.dump(genre_model)

        return genre_dict, 200

    def get_all(self) -> tuple:
        """This method returns all genres found in the genre table

        :returns:
            a tuple including a list of all genres and a status code of
            the operation
        """
        genre_models = self.dao.get_all()

        if not genre_models:
            return 'Not Found', 404

        genre_list = self.schema.dump(genre_models, many=True)

        return genre_list, 200

    def create(self, genre_d: dict) -> tuple:
        """This method creates a new record in the genre table

        :param genre_d: a dictionary with new movie's data

        :returns:
            a tuple with a result of the operation
        """
        try:
            created = self.dao.create(genre_d)

        except Exception as e:
            print(f'При создании новой записи возникла ошибка {e}')
            return 'Bad Request', 400

        location = {'location': f'/genres/{created.id}'}

        return self.schema.dump(created), 201, location

    def update(self, genre_id: int, genre_d: dict) -> tuple:
        """This method updates a record in the genre table

        :param genre_id: the id of the updated genre
        :param genre_d: a dictionary with movie's data to update

        :returns:
            a tuple with a result of the operation
        """
        updated = self.dao.get_one(genre_id)

        if not updated:
            return 'Not Found', 404

        if not genre_d:
            return 'Bad Request', 400

        result = self.dao.update(updated, genre_d)

        return self.schema.dump(result), 204

    def delete(self, rid: int) -> tuple:
        """This method deletes a record from the genre table

        :param rid: the id of the deleted genre

        :returns:
            a tuple with a result of the operation
        """
        deleted = self.dao.get_one(rid)

        if not deleted:
            return 'Not Found', 404

        result = self.dao.delete(deleted)

        return self.schema.dump(result), 204
