from typing import Optional

from project.config import PWD_HASH_SALT, PWD_HASH_ITERATIONS
import hashlib

from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_tokens, approve_refresh_token, get_data_from_token, generate_password_hash, \
    compare_passwords
import base64
import hmac

from project.dao.user_Dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao


    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f"User {pk}")

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def create_user(self, login, password):
        return self.dao.create(login, password)


    def get_by_login(self, login):
        return self.dao.get_user_by_login(login)

    def check(self, login, password):
        user = self.get_by_login(login)
        return generate_tokens(email=user.email, password=password, password_hash=user.password)

    def update_token(self, refresh_token):
        return approve_refresh_token(refresh_token)

    def get_user_by_token(self, refresh_token):
        data = get_data_from_token(refresh_token)
        if data:
            return self.get_by_login(data.get('email'))

    def update_user(self, data, refresh_token):
        user = self.get_user_by_token(refresh_token)
        if user:
            self.dao.update_user(login=user.email, data=data)
            return self.get_user_by_token(refresh_token)

    def update_password(self, data, refresh_token):
        user = self.get_user_by_token(refresh_token)
        password_hash = self.get_hash(user.password)
        if user and compare_passwords(password_hash, data.get("password")):
            self.dao.update_user(login=user.email, data={"password": generate_password_hash(data.get("password_2"))})
            return self.check(login=user.email, password=data.get("password_2"))
    def get_hash(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ).decode("utf-8", "ignore")

    def generate_password(self, password):
        hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),  # Convert the password to bytes
        PWD_HASH_SALT,
        PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash)

    def compare_passwords(self, password_hash, other_password) -> bool:
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode(),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(decoded_digest, hash_digest)
