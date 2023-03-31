from User import User
from Utils.Exceptions import *


class UserController:
    def __init__(self):
        self.users: dict[str, User] = dict()
        self.user_id = 0
        self.connected_users: dict[int, User] = dict()

    def login(self, username: str, password: str) -> User:
        user = self.__get_user_by_user_name(username)
        user.login(password)
        return user

    def __register_user_userid(self, user: User):
        self.connected_users.update({self.user_id: user})
        self.user_id += 1

    def register(self, username: str, password: str) -> User:
        if username in self.users:
            raise DuplicateUserName(username)
        user = User(username, password)
        self.users.update({username: user})
        return user

    def __get_user_by_user_name(self, username: str) -> User:
        if not (username in self.users):
            raise UsernameDoesntExistException(username)
        else:
            return self.users.get(username)

    def __get_user_by_userid(self, userid: int) -> User:
        if not (userid in self.connected_users):
            raise MissingUserID(userid)
        else:
            return self.connected_users.get(userid)
