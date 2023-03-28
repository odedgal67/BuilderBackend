from User import User
from Utils.Exceptions import UsernameDoesntExistException, DuplicateUserName


class UserController:
    def __init__(self):
        self.users: dict[str, User] = dict()

    def login(self, username: str, password: str) -> User:
        user = self.__get_user(username)
        user.login(password)
        return user

    def register(self, username: str, password: str) -> User:
        if username in self.users:
            raise DuplicateUserName(username)
        user = User(username, password)
        self.users.update({username: user})
        return user

    def __get_user(self, username: str) -> User:
        if not (username in self.users):
            raise UsernameDoesntExistException(username)
        else:
            return self.users.get(username)
