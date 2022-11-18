"""This unit contains the DirectorService provides a business logic to serve
user's requests"""
from dao.director import DirectorDAO
from dao.model.director import DirectorSchema
# ------------------------------------------------------------------------


class DirectorService:
    """The DirectorService provides a business logic to work with the
    director table"""
    def __init__(self, dao: DirectorDAO, schema: DirectorSchema) -> None:
        """The initialization of the DirectorService

        :param dao: an instance of the DirectorDAO class
        :param schema: an instance of the DirectorSchema class
        """
        self.dao = dao
        self.schema = schema

    def get_one(self, bid: int) -> tuple:
        """This method returns a single director found by the given bid

        :param bid: the id of the searching director

        :returns:
            a tuple containing the dictionary with the director data and
            the status code of the operation
        """
        director_model = self.dao.get_one(bid)

        if not director_model:
            return 'Not Found', 404

        director_dict = self.schema.dump(director_model)

        return director_dict, 200

    def get_all(self) -> tuple:
        """This method returns a list of all directors

        :returns:
            a tuple containing the list of dictionaries and the status code of
            the operation
        """
        director_models = self.dao.get_all()

        if not director_models:
            return 'Not Found', 404

        directors_list = self.schema.dump(director_models, many=True)

        return directors_list, 200

    def create(self, director_d: dict) -> tuple:
        """This method creates a new record in the director table

        :param director_d: a dictionary with a new director's data

        :returns:
            a tuple containing the result of the operation
        """
        try:
            result = self.dao.create(director_d)

        except Exception as e:
            print(f'При создании записи возникла ошибка {e}')
            return 'Bad Request', 400

        location = {'location': f'/directors/{result.id}'}

        return self.schema.dump(result), 201, location

    def update(self, director_id: int, director_d: dict) -> tuple:
        """This method updates a record in the director table

        :param director_id: the id of the updated record
        :param director_d: a dictionary with data to update

        :returns:
            a tuple containing the result of the operation
        """
        updated = self.dao.get_one(director_id)

        if not updated:
            return 'Not Found', 404

        if not director_d:
            return 'Bad Request', 400

        result = self.dao.update(updated, director_d)

        return self.schema.dump(result), 204

    def delete(self, rid: int) -> tuple:
        """This method deletes a record from the director table

        :param rid: the id of the deleted record

        :returns:
            a tuple containing the result of the operation
        """
        deleted = self.dao.get_one(rid)

        if not deleted:
            return 'Not Found', 404

        result = self.dao.delete(deleted)

        return self.schema.dump(result), 204
