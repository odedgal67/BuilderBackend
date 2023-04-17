from Utils.PasswordHasher import *
from Utils.Exceptions import *


class User:
    def __init__(self, username: str, password: str):
        self.__check_password(password)
        self.__check_username(username)
        self.username = username
        self.hashed_password = hash_password(password)
        self.logged_in = False

    def __check_password(self, password: str) -> str:
        upperandlower = password.isupper() or password.islower()
        if len(password) < 8 or len(password) > 20 or upperandlower:
            raise IllegalPasswordException()
        return password

    def __check_username(self, username: str) -> str:
        if len(username) != 9 or not username.isnumeric():
            raise IllegalUsernameException(username)
        return username

    def login(self, password: str) -> bool:
        if self.logged_in:
            raise AlreadyLoggedException(self.username)
        if not compare_password(password, self.hashed_password):
            raise IncorrectPasswordException()
        self.logged_in = True
        return True
