import base64
import hashlib

from constants import PWD_HASH_ITERATIONS, PWD_HASH_SALT
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_name(self, username):
        return self.dao.get_by_name(username)

    def create(self, user_data):

        password = user_data.get('password')
        hash_pass = self.get_hash(password)
        user_data['password'] = hash_pass

        return self.dao.create(user_data)

    def delete(self, uid):
        self.dao.delete(uid)

    def update(self, user_data):
        self.dao.update(user_data)

    def get_hash(self, password):
        hashed_password = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS)

        return base64.b64encode(hashed_password)