from project.dao.base import BaseDAO
from project.models import User
from project.tools.security import generate_password_hash


class UserDAO(BaseDAO[User]):
    __model__ = User

    def create(self, login, password):
        try:
            self._db_session.add(User(email=login, password=generate_password_hash(password))
                                 )
            self._db_session.commit()
            print("User is created")
        except Exception as e:
            print(e)
            self._db_session.rollback()



    # def get_one(self, bid):
    #     return self.session.query(User).get(bid)
    #
    # def get_all(self):
    #     return self.session.query(User).all()

    #def create(self, user_d):
      #  ent = User(**user_d)
       # self.session.add(ent)
       # self.session.commit()
       # return ent

    # def get_by_username(self, username):
    #     return self.session.query(User).filter(User.username == username).first()


    # def delete(self, rid):
    #     user = self.get_one(rid)
    #     self.session.delete(user)
    #     self.session.commit()

    # def update(self, user_d):
    #     user = self.get_one(user_d.get("id"))
    #     user.name = user_d.get("name")
    #     user.password = user_d.get("password")
    #
    #     self.session.add(user)
    #     self.session.commit()

    def get_user_by_login(self, login):
        try:
            stmt = self._db_session.query(self.__model__).filter(self.__model__.email == login).one()
            return stmt
        except Exception as e:
            print(e)
            return {}

    def update_user(self, login, data):
        try:
            self._db_session.query(self.__model__).update(
                data)
            self._db_session.commit()
            print("Пользователь обновлен")
        except Exception as e:
            print(e)
            self._db_session.rollback()