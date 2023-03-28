from Utils.PasswordHasher import *
from Utils.Exceptions import *


class User:
    def __init__(self, username: str, password, id: str):
        self.username = username
        self.hashed_password = hash_password(password)
        self.id = id
        self.logged_in: bool = False

    def is_correct_password(self, password: str):
        """Compares the password with the hashed password of the user"""
        return hash_password(password) == self.hashed_password

    def is_logged(self):
        return self.logged_in

    def login(self):
        """Logs the user in. If the user is already logged in raises AlreadyLoggedException"""
        if self.is_logged():
            raise AlreadyLoggedException(self.username)
        self.is_logged = True
