from project.dao.base import BaseDAO
from project.models import Genre, Director, Movie
from sqlalchemy import desc
from werkzeug.exceptions import NotFound
class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_order_by(self, page, filter):
        stat = self._db_session.query(self.__model__)
        if filter:
            stat = stat.order_by(desc(self.__model__.year))
        if page:
            try:
                return stat.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stat.all()
