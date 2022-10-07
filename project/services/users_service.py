from project.constaints import PWD_HASH_SALT, PWD_HASH_ITERATIONS
import hashlib

import base64
import hmac

from project.dao.user_Dao import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        return self.dao.create(user_d)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def update(self, user_d):
        user_d["password"] = self.generate_password(user_d["password"])
        return self.dao.update(user_d)

    def delete(self, rid):
        self.dao.delete(rid)

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